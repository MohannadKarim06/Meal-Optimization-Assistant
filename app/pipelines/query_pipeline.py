import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_handler import FileHandler
from utils.logger import log_event
from app.api.openai_client import chat_with_gpt
from utils.token_handler import build_prompt_within_limit
from utils.config_handler import ConfigHandler
file_handler = FileHandler()

def query_pipeline(user_query: str) -> str:
    config = ConfigHandler().load_config()
    base_prompt = config.get("base_prompt")
    
    try:
        log_event("PROCESS", "Searching for relevant content from all indexes.")
        relevant_chunks = file_handler.search_all_indexes(user_query)
        log_event("SUCCESS", f"Found {len(relevant_chunks)} relevant chunks.")
    except Exception as e:
        log_event("ERROR", f"An error occurred during search: {e}")
        raise e

    try:
        log_event("PROCESS", "Building prompt with retrieved chunks.")
        full_system_prompt, user_query = build_prompt_within_limit(
            relevant_chunks, user_query, base_prompt
        )
        log_event("SUCCESS", "Prompt built successfully.")
    except Exception as e:
        log_event("ERROR", f"An error occurred while building the prompt: {e}")
        raise e

    try:
        log_event("PROCESS", "Sending query to GPT.")
        response = chat_with_gpt(full_system_prompt, user_query)
        log_event("SUCCESS", "Received response from GPT.")
        log_event("INFO", f": Full System prompt 'Base prompt + Chunks':\n\n{full_system_prompt}\n\nUser Query:\n\n{user_query}\n\nGPT output:\n\n{response}")
        return response
    except Exception as e:
        log_event("ERROR", f"An error occurred while querying GPT: {e}")
        raise e
