from algo import run, Config
import os
import json

if __name__ == "__main__":
	with open(os.environ['ABOUND_CONFIG_PATH']) as f:
		cfg = Config.from_json(f.read())
	image = run(cfg)
	image.save(os.environ['ABOUND_OUTPUT_PATH'])