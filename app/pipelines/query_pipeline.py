from utils.file_handler import FileHandler
from utils.logger import log_event
from app.api.openai_client import chat_with_gpt
from utils.token_handler import build_prompt_within_limit
from config import ConfigManger

file_handler = FileHandler()
config = ConfigManger()

def query_pipeline(user_query: str) -> str:
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
            relevant_chunks, user_query,base_prompt =  config.base_prompt()
        )
        log_event("SUCCESS", "Prompt built successfully.")
    except Exception as e:
        log_event("ERROR", f"An error occurred while building the prompt: {e}")
        raise e

    try:
        log_event("PROCESS", "Sending query to GPT.")
        response = chat_with_gpt(full_system_prompt, user_query)
        log_event("SUCCESS", "Received response from GPT.")
        return response
    except Exception as e:
        log_event("ERROR", f"An error occurred while querying GPT: {e}")
        raise e
