import openai
from typing import List

from config import ConfigManger
from utils.logger import log_event

config = ConfigManger()
openai.api_key = config.openai_api_key()

CHAT_MODEL = config.chat_model_name()
EMBEDDING_MODEL = config.embedding_model_name()

def chat_with_gpt(system_prompt: str, user_query: str) -> str:
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
