import json
from luau.roblox import write_script
from src.config import get_config

def build_client(config_path: str):
	config_data = get_config(config_path)
	print("CLIENT", json.dumps(config_data, indent=5))

def build_server(config_path: str):
	config_data = get_config(config_path)
	print("SERVER", json.dumps(config_data, indent=5))

def main(config_path: str):
	build_server(config_path)
	build_client(config_path)