import sys
import os
import multiprocessing
from src.config import set_config
from src.build import main as build

def main():
	config_path = "network.json"
	if 1 in sys.argv:
		if sys.argv[1] == "init":
			if 2 in sys.argv:
				config_path = sys.argv[2]
			assert not os.path.exists(config_path), f"{config_path} already exists"
			set_config(config_path)
			return
		else:
			config_path = sys.argv[1]

	build(config_path)

# prevent from running twice
if __name__ == '__main__':
	multiprocessing.freeze_support()
	main()

