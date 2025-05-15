import os

FILES_DIR = "/app/data/files"
CHUNKS_DIR = "/app/data/chunks"
INDEX_DIR = "/app/data/indexes"
CONFIG_PATH = "/app/data/config.json"
LOGS_FILE = "/app/data/logs/logs.log"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_FILE_EXTENSIONS = [".pdf"]

os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOGS_FILE), exist_ok=True)

query_type_prompt = """
Classify the user input into exactly ONE of these categories:
    0: FOOD OR BEVERAGE query (examples: "2 rotis with dal", "chicken pasta", "250ml OJ", "coffee with sugar", "vodka & cola")
    1: GREETING (examples: "Hi", "Hello", "Namaste", "Good morning", "Hey there")
    2: OTHER (not food/beverage or greeting - includes requests for dataset, tests, asking "what foods", health questions, diet plans, etc.)
    
    ONLY return the number (0, 1, or 2) with no additional text or explanation.
    """

meal_type_prompt = """
You are a blood glucose response expert. Your task is to classify the meal or beverage into exactly ONE of these categories:

- TYPE A MEALS: Refined grains/flours, starchy staples, sugars, juices, large portions
- TYPE B MEALS: Moderate whole grains, legumes as main, small portions balanced with protein
- TYPE C MEALS: Mainly protein/fat with non-starchy vegetables, minimal starchy components
- TYPE D MEALS: Almost exclusively protein, fats, non-starchy vegetables, unsweetened beverages

ONLY return the letter A, B, C, or D with no explanation or additional text.
"""