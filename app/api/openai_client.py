import os, sys
import openai
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config_handler import ConfigHandler
from app.config import OPENAI_API_KEY
from utils.logger import log_event

openai.api_key = OPENAI_API_KEY


def chat_with_gpt(system_prompt: str, user_query: str) -> str:
    config = ConfigHandler().load_config()
    CHAT_MODEL = config.get("chat_model")

    try:
        log_event("PROCESS", "Sending message to OpenAI GPT.")

        response = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7
        )

        message = response["choices"][0]["message"]["content"]
        log_event("SUCCESS", "Received response from OpenAI GPT.")
        return message

    except Exception as e:
        log_event("ERROR", f"Error in chat_with_gpt: {e}")
        raise e


def embed_text(text: str) -> List[float]:
    config = ConfigHandler().load_config()
    EMBEDDING_MODEL = config.get("embedding_model")

    try:
        log_event("PROCESS", "Generating embeddings using OpenAI.")

        response = openai.Embedding.create(
            model=EMBEDDING_MODEL,
            input=text
        )

        embedding = response["data"][0]["embedding"]
        log_event("SUCCESS", "Embedding generated successfully.")
        return embedding

    except Exception as e:
        log_event("ERROR", f"Error in embed_text: {e}")
        raise e
