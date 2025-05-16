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

- TYPE A MEALS: Refined grains/flours, starchy staples, sugars, juices, large portions, ANY alcoholic beverages
  * Examples: white rice, white bread, pasta, naan, potatoes, sodas, fruit juices, desserts, ice cream, 
    whiskey, vodka, beer, wine, cocktails, mixed drinks (ANY alcoholic drink regardless of mixer)

- TYPE B MEALS: Moderate whole grains, legumes as main, small portions balanced with protein, milk and milk alternatives
  * Examples: brown rice with chicken, whole wheat roti with dal, oatmeal with nuts, quinoa bowl, 
    dairy milk, oat milk, almond milk, soy milk, other plant-based milks

- TYPE C MEALS: Mainly protein/fat with non-starchy vegetables, minimal starchy components
  * Examples: chicken salad, fish with vegetables, paneer with greens, tofu stir-fry

- TYPE D MEALS: Almost exclusively protein, fats, non-starchy vegetables, unsweetened clear beverages
  * Examples: grilled chicken, seekh kebab, boti kebab, grilled mushroom, soya chaap, paneer tikka, 
    grilled chicken with spinach, boiled eggs with salad, unsweetened black coffee or tea, water

Special classification rules:
1. ALWAYS classify ANY alcoholic beverages (whiskey, vodka, beer, wine, etc.) as Type A, regardless of mixers
2. ALWAYS classify ANY milk or milk alternatives (dairy milk, oat milk, almond milk, etc.) as Type B
3. ALWAYS classify protein-based dishes with non-starchy vegetables (like grilled chicken with spinach) as Type D
4. Plain water, black coffee, and unsweetened tea are Type D beverages
5. When in doubt between Type C and Type D for high-protein meals, prefer Type D

ONLY return the letter A, B, C, or D with no explanation or additional text.
"""