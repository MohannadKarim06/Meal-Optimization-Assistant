import tiktoken
from typing import List, Tuple, Dict

from config import ConfigManger
from utils.logger import log_event

config = ConfigManger()
TOKEN_LIMIT = config.token_limit()
EMBEDDING_MODEL_NAME = config.embedding_model_name()

class TokenHandler:
    def __init__(self):
        self.tokenizer = tiktoken.encoding_for_model(EMBEDDING_MODEL_NAME)


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

            system_tokens = self.count_tokens(base_prompt)
            query_tokens = self.count_tokens(user_query)
            available_tokens = TOKEN_LIMIT - system_tokens - query_tokens

            if available_tokens <= 0:
                log_event("ERROR", "Token limit exceeded by prompt and query alone.")
                raise ValueError("Prompt and query exceed the token limit.")

            final_chunks = []
            total_chunk_tokens = 0

            for chunk, _score in retrieved_chunks:
                chunk_text = f"## {chunk['title']}\n{chunk['content']}"
                chunk_tokens = self.count_tokens(chunk_text)

                if total_chunk_tokens + chunk_tokens > available_tokens:
                    break

                final_chunks.append(chunk)
                total_chunk_tokens += chunk_tokens

            context_text = self.format_chunks(final_chunks)
            full_system_prompt = f"{base_prompt}\n\n{context_text}"

            log_event("SUCCESS", f"Prompt built successfully with {len(final_chunks)} chunks.")
            return user_query, full_system_prompt

        except Exception as e:
            log_event("ERROR", f"Error while building prompt: {e}")
            raise e                   
                
                          