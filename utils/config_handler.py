import json
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import CONFIG_PATH

default_config = {
    "chat_model_name": "gpt-4-turbo",
    "embedding_model_name": "text-embedding-ada-002",
    "base_prompt": "You are a helpful assistant.",
    "top_k_results": 5,
    "token_limit": 8000,
    "follow_ups_prompt": "You are a helpful assistant answering a follow up question...",
    "type_d_limit": False,
    "follow_ups_limit": True
    
}


if not os.path.exists(CONFIG_PATH):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(default_config, f, indent=4)

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
