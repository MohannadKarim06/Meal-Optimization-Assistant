import os

FILES_DIR = "/app/data/files"
CHUNKS_DIR = "/app/data/chunks"
INDEX_DIR = "/app/data/indexes"
CONFIG_PATH = "/app/data/config.json"
LOG_FILE = "/app/data/logs.log"
OPENAI_API_KEY = "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"
ALLOWED_FILE_EXTENSIONS = [".pdf"]

os.makedirs(FILES_DIR, exist_ok=True)
