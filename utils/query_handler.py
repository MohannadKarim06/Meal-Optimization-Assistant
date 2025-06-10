import os, sys, re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.openai_client import chat_with_gpt 
from utils.logger import log_event
from utils.config_handler import ConfigHandler
from utils.token_handler import TokenHandler
from utils.file_handler import FileHandler

file_handler = FileHandler()
token_handler = TokenHandler()

class PipelineReturn(Exception):

    def __init__(self, value, counts_toward_limit):
        self.value = value
        self.counts_toward_limit = counts_toward_limit
        super().__init__(f"Pipeline early return with value: {value}")



class QueryHandler():

    def sanitize_query(self, query: str) -> str:
        sanitized = query.replace("&", "and")
        
        sanitized = re.sub(r'[^\w\s.,?!:;()\[\]{}\'"-]', ' ', sanitized)
        
        sanitized = ' '.join(sanitized.split())
        
        if sanitized != query:
            log_event("INFO", f"Query sanitized: '{query}' -> '{sanitized}'")
        
        return sanitized

    def identify_query(self, query, prompt, temp, chat_history):
        config = ConfigHandler().load_config()
        follow_ups_limit = config.get("follow_ups_limit", True)
        follow_ups_prompt = config.get("follow_ups_prompt", "")

        if chat_history:
            chat_history = token_handler.trim_chat_history(chat_history=chat_history)
        
        response = chat_with_gpt(system_prompt=prompt, user_query=query, temp=temp, max_tokens=1, chat_history=chat_history)
        log_event("SUCCESS", f"Query is {response}")
        if str(response) == "2":
            response = "I need a specific meal to optimize. What are you eating/drinking today?"
            raise PipelineReturn(value=response, counts_toward_limit=False)

        elif str(response) == "1":
            response = "Hey hey! Good to see you here 😄\nI need a specific meal or beverage to optimize. What exactly are you eating or drinking?"        
            raise PipelineReturn(value=response, counts_toward_limit=False)
        
        elif str(response) == "3":
            log_event("PROCESS", "Query is a follow up, Getting response...")
            data_chunks = file_handler.followup_search(query=query)
            follow_up_full_prompt = f"{follow_ups_prompt}\n\n{data_chunks}" 
            response = chat_with_gpt(system_prompt=follow_up_full_prompt, user_query=query, temp=0.6, chat_history=chat_history)
            log_event("SUCCESS", "Response to follow up is generated.")
            
            raise PipelineReturn(value=response, counts_toward_limit=follow_ups_limit)

        elif str(response) == "0":
            return None
        
        else:
            response = "I need a specific meal to optimize. What are you eating/drinking today?"
            raise PipelineReturn(value=response, counts_toward_limit=False)

    def get_type(self, query, prompt, temp):
        config = ConfigHandler().load_config()
        type_d_limit = config.get("type_d_limit", False)
        
        response = chat_with_gpt(system_prompt=prompt, user_query=query, temp=temp, max_tokens=1)

        if response == "D":
            response = "Excellent choice!\nThis is already excellent for blood sugar! Nothing to modify here.\nEnjoy and savor every moment."
            raise PipelineReturn(value=response, counts_toward_limit=type_d_limit)
        
        return response
    

    def get_final_response(self, query, prompt, temp, type):
        full_prompt = f"You are analyzing a Type {type}. NEVER NEVER mention this type to the user.\n\n{prompt}"

        response = chat_with_gpt(system_prompt=full_prompt, user_query=query, temp=temp, max_tokens=None)
        log_event("INFO", f": User Query:\n\n{query}\n\nFull System prompt 'Base prompt + Chunks':\n\n{full_prompt}\n\nGPT output:\n\n{response}")

        return response