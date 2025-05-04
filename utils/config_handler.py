import json
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import CONFIG_PATH

class ConfigHandler:
    def __init__(self, path=CONFIG_PATH):
        self.path = path

    def load_config(self):
        with open(self.path, 'r') as f:
            return json.load(f)

    def save_config(self, config_data: dict):
        with open(self.path, 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_config(self, updates: dict):
        config = self.load_config()
        config.update(updates)
        self.save_config(config)
        return config
