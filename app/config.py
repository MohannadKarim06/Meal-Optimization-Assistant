import os

FILES_DIR = "/app/data/files"
CHUNKS_DIR = "/app/data/chunks"
INDEX_DIR = "/app/data/indexes"
CONFIG_PATH = "/app/data/config.json"
LOGS_FILE = "/app/data/logs/logs.log"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_FILE_EXTENSIONS = [".pdf"]

os.makedirs(FILES_DIR, exist_ok=True)
