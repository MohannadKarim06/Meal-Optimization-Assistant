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
from utils.logger import log_event

from app.config import FILES_DIR, CHUNKS_DIR, INDEX_DIR


class FileHandler:
    def __init__(self):
        config = ConfigHandler().load_config()
        self.TOP_K_RESULTS = config.get("top_k_results")
        self.SIMILARITY_THRESHOLD = config.get("similarity_threshold", 0.6)


    def extract_text_from_pdf(self, file_name: str) -> str:
        file_path = os.path.join(FILES_DIR, f"{file_name}.pdf")
        full_text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                full_text += page.get_text()
        return full_text


    def chunk_text(self, full_text: str, file_name: str) -> List[Dict]:
        sections = full_text.split("Section: ")
        if len(sections) < 2:
            raise ValueError("Expected 'Section: ' markers not found in PDF text.")

        chunks = []

        first_section = sections[1]
        title_end = first_section.find("\n")
        general_title = first_section[:title_end].strip()
        general_rules = first_section[title_end + 1:].strip()

        general_chunk = f"from file: {file_name}.pdf\n\n## {general_title}\n{general_rules}"
        chunks.append({
            "id": str(uuid4()),
            "title": general_title,
            "content": general_chunk
        })

        for section in sections[2:]:
            title_end = section.find("\n")
            title = section[:title_end].strip()
            content = section[title_end + 1:].strip()

            full_chunk = f"from file: {file_name}.pdf\n\n{general_rules}\n\n## {title}\n{content}"
            chunks.append({
                "id": str(uuid4()),
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
        
        index = faiss.IndexFlatIP(dimension)
        
        vectors_np = np.array(vectors).astype("float32")
        faiss.normalize_L2(vectors_np)
        
        index.add(vectors_np)

        index_path = os.path.join(INDEX_DIR, f"{file_name}_index.index")
        faiss.write_index(index, index_path)

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
        log_event("PROCESS", "Generating embedding for search query")
        query_vector = embed_text(query)
        query_vector_np = np.array([query_vector]).astype("float32")
        
        faiss.normalize_L2(query_vector_np)
        
        all_results = []
        filtered_results = []

        log_event("PROCESS", f"Searching through indexes with similarity threshold: {self.SIMILARITY_THRESHOLD}")
        for index_file in os.listdir(INDEX_DIR):
            if not index_file.endswith(".index"):
                continue

            file_name = index_file.replace("_index.index", "")
            chunk_path = os.path.join(CHUNKS_DIR, f"{file_name}_chunks.json")

            if not os.path.exists(chunk_path):
                continue

            try:
                with open(chunk_path, "r", encoding="utf-8") as f:
                    chunk_data = json.load(f)
                
                index = faiss.read_index(os.path.join(INDEX_DIR, index_file))

                search_k = min(self.TOP_K_RESULTS * 3, 50)  
                distances, indices = index.search(query_vector_np, search_k)

                for i, score in zip(indices[0], distances[0]):
                    if i == -1:
                        continue  
                    
                    if score < self.SIMILARITY_THRESHOLD:
                        continue  
                    
                    chunk_ids = list(chunk_data.keys())
                    if i < len(chunk_ids):
                        chunk_id = chunk_ids[i]
                        chunk = chunk_data.get(chunk_id)
                        if chunk:
                            all_results.append((chunk, float(score)))
            
            except Exception as e:
                log_event("ERROR", f"Error searching index {file_name}: {e}")
                continue

        all_results.sort(key=lambda x: x[1], reverse=True)
        
        filtered_count = len(all_results)
        final_results = all_results[:self.TOP_K_RESULTS]
        
        log_event("SUCCESS", f"Found {filtered_count} relevant results (score >= {self.SIMILARITY_THRESHOLD})")
        return final_results
    

    def followup_search(self, query, max_chunks:int=5, threshold:float=0.8):

        query_vector = embed_text(query)
        query_vector_np = np.array([query_vector]).astype("float32")

        faiss.normalize_L2(query_vector_np)

        all_results = []

        for index_file in os.listdir(INDEX_DIR):
            if not index_file.endswith(".index"):
                continue


            file_name = index_file.replace("_index.index", "")
            chunks_path = os.path.join(CHUNKS_DIR, f"{file_name}_chunks.json")

            if not os.path.exists(chunks_path):
                continue

            index_path = os.path.join(INDEX_DIR, index_file)

            with open(chunks_path, "r", encoding="utf-8") as f:
                chunks_data = json.load(f)

            index = faiss.read_index(index_path)

            search_k = min(max_chunks * 4, 50)  

            distances, indices = index.search(query_vector_np, search_k)  

            for i, score in zip(indices[0], distances[0]):

                if i == -1:
                    continue


                if score < threshold:
                    continue

                chunk_ids = list(chunks_data.keys())

                if i < len(chunk_ids):
                    chunk_id = chunk_ids[i]
                    chunk = chunks_data.get(chunk_id)
                    if chunk:
                        all_results.append((chunk, float(score)))

        all_results.sort(key=lambda x: x[1], reverse=True)

        final_reesults = all_results[:max_chunks]

        return final_reesults


             


