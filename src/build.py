import json
import os
import sys
import dpath
from luau.roblox import write_script, get_module_require
from luau import indent_block
from src.config import get_config, ParameterData, FunctionData, PortData, Any

BINDABLE_EVENT_KEY = "on_event"
BINDABLE_FUNC_KEY = "on_invoke"

REMOTE_EVENT_CLIENT_KEY = "on_client_event"
REMOTE_EVENT_SERVER_KEY = "on_server_event"

REMOTE_EVENT_KEYS = [
	REMOTE_EVENT_SERVER_KEY,
	REMOTE_EVENT_CLIENT_KEY
]

REMOTE_FUNCTION_SERVER_KEY = "on_server_invoke"
REMOTE_FUNCTION_CLIENT_KEY = "on_client_invoke"

REMOTE_FUNCTION_KEYS = [
	REMOTE_FUNCTION_SERVER_KEY,
	REMOTE_FUNCTION_CLIENT_KEY,
]

CONSTRUCTOR_KEYS = REMOTE_FUNCTION_KEYS + REMOTE_EVENT_KEYS + [
	BINDABLE_EVENT_KEY,
	BINDABLE_FUNC_KEY
]

SIMPLE_TYPES = [
	"number",
	"string",
	"boolean",
	# "nil",
	# "table",
	# "vector",
	# "function",
	# "thread",
	# "userdata"
]


def get_assertion(type_name: str, var_name: str, type_name_list: list[str]) -> str:
	conditions = []


	if "?" in type_name:
		conditions.append(f"({var_name} ~= nil)")
		type_name = type_name.replace("?", "")

	if type_name in SIMPLE_TYPES:
		conditions.append(f"(type({var_name}) == \"{type_name}\")")
	elif (not type_name in type_name_list) and (not "{" in type_name):
		conditions.append(f"(typeof({var_name}) == \"{type_name}\")")


	assertion = "assert(" + " and ".join(conditions) + ")"
	return assertion


def get_class_name(data: PortData) -> str:
	if "on_server_event" in data or "on_client_event" in data:
		return "RemoteEvent"
	elif "on_server_invoke" in data or "on_client_invoke" in data:
		return "RemoteFunction"
	elif "on_event" in data:
		return "BindableEvent"
	elif "on_invoke" in data:
		return "BindableFunction"

	raise ValueError("Bad port data: "+json.dumps(data))



def get_package_zip_path(is_verbose: bool=False) -> str:
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	# print("\nBASE", base_path)
	# for sub_path in os.listdir(base_path):
	# 	print(sub_path)

	zip_path = os.path.join(base_path, "data\\Packages.zip").replace("\\", "/")
	assert os.path.exists(zip_path), f"package zip path {zip_path} does not exist"
	if is_verbose:
		print(f"zip package exists: {zip_path}", os.path.exists(zip_path))
	return zip_path

def build_client(config_path: str):
	config_data = get_config(config_path)
	print("CLIENT", json.dumps(config_data, indent=5))

def build_server(config_path: str):
	config_data = get_config(config_path)
	build_path = config_data["build"]["server_path"]
	print("SERVER", json.dumps(config_data, indent=5))
	type_name_list: list[str] = []
	type_imports: list[str] = []
	module_requires:list[str] = []
	for type_data in config_data["type_imports"]:
		type_name = type_data["name"]
		type_path = type_data["path"]
		type_name_list.append(type_name)
		module_requires.append(f"local {type_name} = {get_module_require(type_path)}")
		type_imports.append(f"export type {type_name} = {type_name}.{type_name}")

	port_registry: dict[str, PortData] = {}

	for path, data in dpath.search(config_data["tree"], '**', yielded=True):
		if isinstance(data, dict):
			for key in CONSTRUCTOR_KEYS:
				if key in data:
					untyped_data: Any = data
					port_registry[path] = untyped_data

	print(json.dumps(port_registry, indent=5))

	private_functions: list[str] = []
	for path, data in port_registry.items():
		for call_name, call_data in data.items():
			call_name = call_name.replace("_", " ").title().replace(" ", "")

			# start function
			function_path_name = path.replace("/", "")
			function_name = call_name + function_path_name
			function_name = function_name[0].lower()+function_name[1:]

			# unpack types
			type_param_lines = []
			untyped_param_lines = []
			type_return_lines = []
			assertion_list = []
			if "parameters" in call_data:
				for param_data in call_data["parameters"]:
					name = param_data["name"]
					type_name = param_data["type"]
					assertion_list.append(get_assertion(type_name, name, type_name_list))
					type_param_lines.append(f"{name}: {type_name}")
					untyped_param_lines.append(name)

			if "returns" in call_data:
				for return_type in call_data["returns"]:
					type_return_lines.append(return_type)

			function_lines = [
				f"\nlocal function {function_name}(",
				",".join(type_param_lines),
				"): ("+",".join(type_return_lines)+")\n"
			]

			# add meat
			function_lines += indent_block(assertion_list)


			# end and add function
			function_lines.append("end")

			private_functions += function_lines





	content_lines: list[str] = [
	"--!strict",
	"-- Services",
	"-- Packages",
	"-- Modules",
	]+module_requires+[
	"\n-- Types",
	]+type_imports+[
	"\n-- Constants",
	"-- Variables",
	"-- References",
	"-- Private functions",
	] + private_functions + [
	"\n-- Class",
	]
	content = "\n".join(content_lines)
	write_script(build_path, content, packages_dir_zip_file_path=get_package_zip_path())

def main(config_path: str):
	build_server(config_path)
	build_client(config_path)