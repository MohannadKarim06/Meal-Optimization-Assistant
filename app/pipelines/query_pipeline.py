import os, sys
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_handler import FileHandler
from utils.logger import log_event
from app.api.openai_client import chat_with_gpt
from app.config import query_type_prompt, meal_type_prompt
from utils.token_handler import TokenHandler
from utils.config_handler import ConfigHandler
from utils.query_handler import QueryHandler, PipelineReturn
query_handler = QueryHandler()
file_handler = FileHandler()
token_handler = TokenHandler()


def query_pipeline(user_query: str) -> str:
    config = ConfigHandler().load_config()
    base_prompt = config.get("base_prompt")
    
    try:
        log_event("PROCESS", "Identifying query.")
        query_handler.identify_query(query=user_query, prompt=query_type_prompt, temp=0.1)
        log_event("SUCCESS", "Query is valid.")
    except PipelineReturn as pr:
        return pr.value
    except Exception as e:
        log_event("ERROR", f"An error occured during getting query type: {e}")
        raise e
    
    try:
        log_event("PROCESS", "Getting meal type.")
        meal_type = query_handler.get_type(query=user_query, prompt=meal_type_prompt, temp=0.1)
        log_event("SUCCESS", f"Meal type is: {meal_type}")
    except PipelineReturn as pr:
        return pr.value
    except Exception as e:
        log_event("ERROR", "An error occured during getting meal type")    
        raise e    

    try:
        log_event("PROCESS", "Sanitizing user query.")
        sanitized_query = query_handler.sanitize_query(user_query)
        log_event("SUCCESS", "Query sanitized successfully.")
        
        log_event("PROCESS", "Searching for relevant content from all indexes.")
        relevant_chunks = file_handler.search_all_indexes(sanitized_query)
        log_event("SUCCESS", f"Found {len(relevant_chunks)}.")

    except Exception as e:
        log_event("ERROR", f"An error occurred during search: {e}")
        raise e
    
    try:
        log_event("PROCESS", "Building prompt with retrieved chunks.")
        full_system_prompt, sanitized_query = token_handler.build_prompt_within_limit(
            base_prompt, sanitized_query, relevant_chunks
        )
        log_event("SUCCESS", "Prompt built successfully.")

    except Exception as e:
        log_event("ERROR", f"An error occurred while building the prompt: {e}")
        raise e

    try:
        log_event("PROCESS", "Sending query to GPT.")
        response = query_handler.get_final_response(prompt=full_system_prompt, query=sanitized_query, temp=0.7, type=meal_type)
        log_event("SUCCESS", "Received response from GPT.")
        log_event("INFO", f": User Query:\n\n{sanitized_query}\n\nFull System prompt 'Base prompt + Chunks':\n\n{full_system_prompt}\n\nGPT output:\n\n{response}")
        return response
    
    except Exception as e:
        log_event("ERROR", f"An error occurred while querying GPT: {e}")
        raise e