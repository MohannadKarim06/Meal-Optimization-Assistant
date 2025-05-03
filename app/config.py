import os

# === Directories ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
FILES_DIR = os.path.join(DATA_DIR, "files")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
LOGS_DIR = os.path.join(DATA_DIR, "logs")

# === Files ===
LOG_FILE = os.path.join(LOGS_DIR, "app.log")

# === Flags / Defaults ===
DEBUG = True
ALLOWED_FILE_EXTENSIONS = [".pdf"]

# Ensure critical directories exist
os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
