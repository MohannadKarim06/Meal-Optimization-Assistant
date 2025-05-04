import os, sys
import json
import fitz  
import faiss
import numpy as np
from uuid import uuid4
from typing import List, Tuple, Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.openai_client import embed_text
from utils.config_handler import ConfigHandler

from app.config import FILES_DIR, CHUNKS_DIR, INDEX_DIR


class FileHandler:
    def __init__(self):
        config = ConfigHandler().load_config()
        self.TOP_K_RESULTS = config.get("top_k_results") 


    def extract_text_from_pdf(self, file_name: str) -> str:
        file_path = os.path.join(FILES_DIR, file_name)
        full_text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                full_text += page.get_text()
        return full_text

    def chunk_text(self, full_text: str) -> List[Dict]:
        sections = full_text.split("Section: ")
        general_rules = sections[0].strip()
        chunks = []

        for section in sections[1:]:
            title_end = section.find("\n")
            if title_end == -1:
                continue

            title = section[:title_end].strip()
            content = section[title_end + 1:].strip()
            full_chunk = f"{general_rules}\n\n## {title}\n{content}"
            chunk_id = str(uuid4())

            chunks.append({
                "id": chunk_id,
                "title": title,
                "content": full_chunk
            })

        return chunks

    def embed_chunks(self, chunks: List[Dict]) -> List[Tuple[str, List[float]]]:
        embeddings = []
        for chunk in chunks:
            vector = embed_text(chunk["content"])
            embeddings.append((chunk["id"], vector))
        return embeddings

    def save_chunks_and_index(self, chunks: List[Dict], embeddings: List[Tuple[str, List[float]]], file_name: str) -> None:
        ids = [chunk["id"] for chunk in chunks]
        vectors = [vec for _, vec in embeddings]

        dimension = len(vectors[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(vectors).astype("float32"))

        # Save FAISS index
        index_path = os.path.join(INDEX_DIR, f"{file_name}_index.index")
        faiss.write_index(index, index_path)

        # Save chunk text
        chunk_path = os.path.join(CHUNKS_DIR, f"{file_name}_chunks.json")
        chunk_data = {chunk["id"]: chunk for chunk in chunks}
        with open(chunk_path, "w", encoding="utf-8") as f:
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)

    def delete_data_files(self, file_name: str) -> None:
        index_path = os.path.join(INDEX_DIR, f"{file_name}_index.index")
        chunk_path = os.path.join(CHUNKS_DIR, f"{file_name}_chunks.json")

        for path in [index_path, chunk_path]:
            if os.path.exists(path):
                os.remove(path)

    def search_all_indexes(self, query: str) -> List[Tuple[Dict, float]]:
        query_vector = embed_text(query)
        query_vector_np = np.array([query_vector]).astype("float32")

        all_results = []

        for index_file in os.listdir(INDEX_DIR):
            if not index_file.endswith(".index"):
                continue

            file_name = index_file.replace("_index.index", "")
            chunk_path = os.path.join(CHUNKS_DIR, f"{file_name}_chunks.json")

            if not os.path.exists(chunk_path):
                continue

            # Load FAISS index
            index = faiss.read_index(os.path.join(INDEX_DIR, index_file))

            # Search top K
            distances, indices = index.search(query_vector_np, self.TOP_K_RESULTS)

            # Load chunk data
            with open(chunk_path, "r", encoding="utf-8") as f:
                chunk_data = json.load(f)

            for i, score in zip(indices[0], distances[0]):
                if i == -1:
                    continue  # No result
                chunk_ids = list(chunk_data.keys())
                if i < len(chunk_ids):
                    chunk_id = chunk_ids[i]
                    chunk = chunk_data.get(chunk_id)
                    if chunk:
                        all_results.append((chunk, float(score)))

        # Sort by score (lower is better in L2 distance)
        all_results.sort(key=lambda x: x[1])
        return all_results[:self.TOP_K_RESULTS]
