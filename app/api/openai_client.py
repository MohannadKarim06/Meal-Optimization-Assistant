import os, sys
from openai import OpenAI
from typing import List
from transformers import AutoTokenizer, AutoModel
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config_handler import ConfigHandler
from app.config import OPENAI_API_KEY
from utils.logger import log_event

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENAI_API_KEY,
)

def chat_with_gpt(system_prompt: str, user_query: str) -> str:
    try:
        log_event("PROCESS", f"Sending message to OpenRouter.")

        response = client.chat.completions.create(
            model="openai/gpt-4-turbo",  
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=1.0
            
        )

        message = response.choices[0].message.content
        log_event("SUCCESS", "Received response from OpenRouter.")
        return message

    except Exception as e:
        log_event("ERROR", f"Error in chat_with_gpt: {e}")
        raise e


model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def embed_text(text: str) -> List[float]:
    config = ConfigHandler().load_config()
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**encoded_input)

        # Mean pooling
    token_embeddings = model_output.last_hidden_state
    attention_mask = encoded_input['attention_mask']
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embedding_vector = (sum_embeddings / sum_mask).squeeze().cpu().numpy().tolist()
    
    return embedding_vector