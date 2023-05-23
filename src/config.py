import yaml
from typing import TypedDict, Any, Literal

class BuildData(TypedDict):
	build_as_service: bool
	client_path: str
	server_path: str

class TreeData(TypedDict):
	remote_event: dict
	remote_function: dict
	bindable_event: dict
	bindable_function: 

class ConfigData(TypedDict):
	build: BuildData
	type_imports: dict[str, str]
	tree: dict

DEFAULT_YAML_FILE = """
build: 
  build_as_service: true
  server_path: out/Server.luau
  client_path: out/Server.luau
type_imports:
  VehicleData: game/ReplicatedStorage/Shared/Vehicle/VehicleData
  PlayerData: game/ServerScriptService/Server/Player/Data
tree:
  remote_event:
    Vehicle:
      OnDestroyed: 
        vehicleId: string
        data: VehicleData
        position: Vector3
  remote_function:
      Vehicle:
      OnDestroyed: 
        vehicleId: string
        data: VehicleData
        position: Vector3
  bindable_event:
  bindable_function:  
"""	

def get_config(config_path: str) -> ConfigData:
	with open(config_path, "r") as config_file:
		config_content = config_file.read()
		return yaml.safe_load(config_content)

def set_config(out_path: str, config_data: ConfigData | None = None):
	config_content = ""
	if config_data != None:
		config_content = yaml.safe_dump(config_data)
	elif config_data == None:
		config_content = DEFAULT_YAML_FILE

	with open(out_path, "w") as config_file:
		config_file.write(config_content)
