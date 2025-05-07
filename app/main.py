from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.pipelines.query_pipeline import query_pipeline
from app.pipelines.file_pipeline import file_upload_pipeline, file_delete_pipeline
from utils.config_handler import ConfigHandler
from utils.logger import log_event
from app.config import FILES_DIR, LOGS_FILE

app = FastAPI(title="Document QA API")

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to restrict access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Config handler
config_handler = ConfigHandler()


@app.get("/")
def root():
    return {"message": "API is running!"}


@app.get("/logs")
def get_logs():
    if not os.path.exists(LOGS_FILE):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(LOGS_FILE, "r") as f:
        logs = f.read()
    return {"logs": logs}



@app.get("/files")
def list_uploaded_files():
    try:
        files = [f.split(".")[0] for f in os.listdir(FILES_DIR) if f.endswith(".pdf")]
        log_event("SUCCESS", f"Retrieved {len(files)} files.")
        return {"files": files}
    except Exception as e:
        log_event("ERROR", f"Failed to list uploaded files: {e}")
        raise HTTPException(status_code=500, detail="Unable to list files")


@app.get("/config")
def get_config():
    try:
        config = config_handler.load_config()
        log_event("SUCCESS", "Configuration retrieved successfully.")
        return config
    except Exception as e:
        log_event("ERROR", f"Failed to load config: {e}")
        raise HTTPException(status_code=500, detail="Unable to load configuration")


@app.post("/ask")
def ask_route(query: str):
    try:
        log_event("PROCESS", "Processing query has started!")
        response = query_pipeline(query)
        log_event("SUCCESS", "Query is processed successfully.")
        return {"response": response}
    except Exception as e:
        log_event("ERROR", f"An error occured while processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")



@app.post("/config")
def update_config(updates: dict):
    try:
        updated_config = config_handler.update_config(updates)
        log_event("SUCCESS", "Configuration updated successfully.")
        return updated_config
    except Exception as e:
        log_event("ERROR", f"Failed to update config: {e}")
        raise HTTPException(status_code=500, detail="Unable to update configuration")


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    filename = os.path.splitext(file.filename)[0]

    file_path = os.path.join(FILES_DIR, f"{filename}.pdf")
    if os.path.exists(file_path):
        log_event("ERROR", f"Upload failed: {filename}.pdf already exists.")
        raise HTTPException(status_code=400, detail="File already exists.")

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        log_event("SUCCESS", f"File {filename}.pdf uploaded successfully.")
        file_upload_pipeline(filename)
        return {"message": f"{filename}.pdf uploaded and processed successfully."}
    except Exception as e:
        log_event("ERROR", f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail="Upload failed. Check logs.")


@app.delete("/delete/{filename}")
def delete_file(filename: str):
    file_path = os.path.join(FILES_DIR, f"{filename}.pdf")

    if not os.path.exists(file_path):
        log_event("ERROR", f"Deletion failed: {filename}.pdf not found.")
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        os.remove(file_path)
        file_delete_pipeline(filename)
        log_event("SUCCESS", f"{filename}.pdf and associated data deleted.")
        return {"message": f"{filename}.pdf deleted successfully."}
    except Exception as e:
        log_event("ERROR", f"Deletion failed for {filename}: {e}")
        raise HTTPException(status_code=500, detail="Deletion failed. Check logs.")
