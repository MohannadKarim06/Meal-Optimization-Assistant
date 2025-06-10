import tiktoken
from typing import List, Tuple, Dict
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config_handler import ConfigHandler
from utils.logger import log_event


class TokenHandler:
    def __init__(self):
        config = ConfigHandler().load_config()
        chat_model_name = config.get("chat_model_name", "gpt-3.5-turbo")  
        self.tokenizer = tiktoken.encoding_for_model(chat_model_name)

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def format_chunks(self, chunks: List[Dict]) -> str:
        return "\n\n".join(
            f"## {chunk['title']}\n{chunk['content']}" for chunk in chunks
        )

    def build_prompt_within_limit(
        self,
        base_prompt: str,
        user_query: str,
        retrieved_chunks: List[Tuple[Dict, float]]
    ) -> Tuple[str, str]:
        try:
            log_event("PROCESS", "Building prompt with token limit handling.")

            config = ConfigHandler().load_config()  
            token_limit = config.get("token_limit", 8000)  



            system_tokens = self.count_tokens(base_prompt)
            query_tokens = self.count_tokens(user_query)
            available_tokens = token_limit - system_tokens - query_tokens

            if available_tokens <= 0:
                log_event("ERROR", "Token limit exceeded by prompt and query alone.")
                raise ValueError("Prompt and query exceed the token limit.")

            final_chunks = []
            total_chunk_tokens = 0

            for chunk, _score in retrieved_chunks:
                title = str(chunk.get('title', '') or '')
                content = str(chunk.get('content', '') or '')

                chunk_text = f"## {title}\n{content}"
                chunk_tokens = self.count_tokens(chunk_text)

                if total_chunk_tokens + chunk_tokens > available_tokens:
                    break

                final_chunks.append({'title': title, 'content': content})
                total_chunk_tokens += chunk_tokens
                
            context_text = self.format_chunks(final_chunks)
            full_system_prompt = f"{base_prompt}\n\n{context_text}"

            log_event("SUCCESS", f"Prompt built successfully with {len(final_chunks)} chunks.")
            return user_query, full_system_prompt

        except Exception as e:
            log_event("ERROR", f"Error while building prompt: {e}")
            raise e


    def trim_chat_history(self, chat_history: List[Dict], max_tokens:int=600):

        if not chat_history:
            return ""
        
        total_tokens = 0

        for message in chat_history:

            role = message.get("role", "")
            content = message.get("content", "")

            message_text = f"{role}: {content}"
            total_tokens += self.count_tokens(message_text)


        if total_tokens <= max_tokens:
            return chat_history

        trimmed_history = chat_history.copy()            
        current_tokens = total_tokens

        while current_tokens > max_tokens and trimmed_history:

            removed_message = trimmed_history[0].pop()

            role = removed_message.get("role", "")
            content = removed_message.get("content", "")

            removed_message_tokens = self.count_tokens(f"{role}: {content}")

            current_tokens -= removed_message_tokens

        return trimmed_history

