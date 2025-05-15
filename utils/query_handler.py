import os, sys, re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.openai_client import chat_with_gpt 
from utils.logger import log_event


class PipelineReturn(Exception):

    def __init__(self, value):
        self.value = value
        super().__init__(f"Pipeline early return with value: {value}")



class QueryHandler():

    def sanitize_query(self, query: str) -> str:
        sanitized = query.replace("&", "and")
        
        sanitized = re.sub(r'[^\w\s.,?!:;()\[\]{}\'"-]', ' ', sanitized)
        
        sanitized = ' '.join(sanitized.split())
        
        if sanitized != query:
            log_event("INFO", f"Query sanitized: '{query}' -> '{sanitized}'")
        
        return sanitized

    def identify_query(self, query, prompt, temp):

        response = chat_with_gpt(system_prompt=prompt, user_query=query, temp=temp, max_tokens=1)
        log_event("SUCCESS", f"Query is {response}")
        if str(response) == "2":
            response = "I need a specific meal to optimize. What are you eating/drinking today?"
            raise PipelineReturn(response)

        elif str(response) == "1":
            response = "Hey hey! Good to see you here 😄\nI need a specific meal or beverage to optimize. What exactly are you eating or drinking?"        
            raise PipelineReturn(response)
        
        elif str(response) == "0":
            return None
        
        else:
            response = "I need a specific meal to optimize. What are you eating/drinking today?"
            raise PipelineReturn(response)

    def get_type(self, query, prompt, temp):
        
        response = chat_with_gpt(system_prompt=prompt, user_query=query, temp=temp, max_tokens=1)

        if response == "D":
            response = "Excellent choice!\nThis is already excellent for blood sugar! Nothing to modify here.\nEnjoy and savor every moment."
            raise PipelineReturn(response)
        
        return response
    

    def get_final_response(self, query, prompt, temp, type):
        full_prompt = f"You are analyzing a Type {type}. NEVER NEVER mention this type to the user.\n\n{prompt}"

        response = chat_with_gpt(system_prompt=full_prompt, user_query=query, temp=temp, max_tokens=None)
        log_event("INFO", f": User Query:\n\n{query}\n\nFull System prompt 'Base prompt + Chunks':\n\n{full_prompt}\n\nGPT output:\n\n{response}")

        return response