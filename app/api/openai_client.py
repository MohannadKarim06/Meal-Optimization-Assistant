from openai import OpenAI
from typing import List

from utils.config_handler import ConfigHandler
from utils.logger import log_event
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def chat_with_gpt(system_prompt: str, user_query: str, temp: float, max_tokens=None) -> str:
    try:
        messages =[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
                
            ]

        config = ConfigHandler().load_config()
        CHAT_MODEL = config.get("chat_model_name")
        log_event("PROCESS", "Sending message to OpenAI GPT.")
        
        if max_tokens:
            response = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=messages,
                temperature=temp,
                max_tokens=max_tokens
            )
        else:
            response = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=messages,
                temperature=temp
            )
        

        message = response.choices[0].message.content
        log_event("SUCCESS", "Received response from OpenAI GPT.")
        return message

    except Exception as e:
        log_event("ERROR", f"Error in chat_with_gpt: {e}")
        raise e


def embed_text(text: str) -> List[float]:
    try:
        config = ConfigHandler().load_config()
        EMBEDDING_MODEL = config.get("embedding_model_name")


        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )

        embedding = response.data[0].embedding
        return embedding

    except Exception as e:
        log_event("ERROR", f"Error in embedding text using OpenAI: {e}")
        raise e