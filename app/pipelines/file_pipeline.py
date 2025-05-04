import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_handler import FileHandler
from utils.logger import log_event

file_handler = FileHandler()


def file_upload_pipeline(file_name: str):
    
    try:
        log_event("PROCESS", "Extracting text from PDF has started!")
        text = file_handler.extract_text_from_pdf(file_name)
        log_event("SUCCESS", "Extracting text from PDF is completed.")
    except Exception as e:
        log_event("ERROR", f"An error occurred while extracting text from PDF: {e}")
        raise e

    try:
        log_event("PROCESS", "Chunking text has started!")
        chunks = file_handler.chunk_text(text)
        log_event("SUCCESS", f"Chunking completed. Total chunks: {len(chunks)}.")
    except Exception as e:
        log_event("ERROR", f"An error occurred while chunking text: {e}")
        raise e

    try:
        log_event("PROCESS", "Embedding chunks has started!")
        embeddings = file_handler.embed_chunks(chunks)
        log_event("SUCCESS", "Embedding completed.")
    except Exception as e:
        log_event("ERROR", f"An error occurred while embedding chunks: {e}")
        raise e

    try:
        log_event("PROCESS", "Saving FAISS index and chunks has started!")
        file_handler.save_chunks_and_index(chunks, embeddings, file_name)
        log_event("SUCCESS", "Saving index and chunks completed.")
    except Exception as e:
        log_event("ERROR", f"An error occurred while saving index and chunks: {e}")
        raise e


def file_delete_pipeline(file_name: str):
    try:
        log_event("PROCESS", f"Attempting to delete index and chunk files for: {file_name}")
        file_handler.delete_data_files(file_name)
        log_event("SUCCESS", f"Files related to {file_name} were deleted successfully.")
    except Exception as e:
        log_event("ERROR", f"An error occurred while deleting files for {file_name}: {e}")
        raise e
