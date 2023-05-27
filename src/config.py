import json
from typing import TypedDict, Any, Literal, Optional

class BuildData(TypedDict):
	build_as_service: bool
	client_path: str
	server_path: str

class ParameterData(TypedDict):
	name: str
	type: str

class TypeData(TypedDict):
	name: str
	path: str

class FunctionData(TypedDict):
	parameters: list[ParameterData]
	returns: list[str]

class EventData(TypedDict):
	parameters: list[ParameterData]

class PortData(TypedDict):
	on_event: Optional[EventData]
	on_server_event: Optional[EventData]
	on_client_event: Optional[EventData]
	on_invoke: Optional[FunctionData]
	on_server_invoke: Optional[FunctionData]
	on_client_invoke: Optional[FunctionData]


class ConfigData(TypedDict):
	build: BuildData
	type_imports: list[TypeData]
	tree: dict[str, PortData]

DEFAULT_JSON_FILE = """
{
	"build": {
		"build_as_service": true,
		"client_path": "out/Client/NetworkTree.luau",
		"server_path": "out/Server/NetworkTree.luau"
	},
	"type_imports": [],
	"tree": {}
}
"""

def get_config(config_path: str) -> ConfigData:
	with open(config_path, "r") as config_file:
		config_content = config_file.read()
		return json.loads(config_content)

def set_config(out_path: str, config_data: ConfigData | None = None):
	config_content = ""
	if config_data != None:
		config_content = json.dumps(config_data, indent=5)
	elif config_data == None:
		config_content = DEFAULT_JSON_FILE

	with open(out_path, "w") as config_file:
		config_file.write(config_content)
