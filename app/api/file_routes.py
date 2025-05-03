import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pipelines.query_pipeline import file_upload_pipeline, file_delete_pipeline
from config import FILES_DIR
from utils.logger import log_event

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(FILES_DIR, file.filename)

    try:
        log_event("PROCESS", f"Checking if file {file.filename} already exists.")

        if os.path.exists(file_path):
            log_event("ERROR", f"Upload failed: {file.filename} already exists.")
            raise HTTPException(status_code=400, detail="File already exists.")

        log_event("PROCESS", f"Saving uploaded file: {file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        log_event("SUCCESS", f"File saved successfully: {file.filename}")
        file_name_without_ext = os.path.splitext(file.filename)[0]

        log_event("PROCESS", f"Starting upload pipeline for: {file_name_without_ext}")
        file_upload_pipeline(file_name_without_ext)
        log_event("SUCCESS", f"Upload pipeline completed for: {file_name_without_ext}")

        return {"message": f"{file.filename} uploaded and processed successfully."}

    except Exception as e:
        log_event("ERROR", f"Upload route failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.delete("/delete")
def delete_file(file_name: str):
    file_path = os.path.join(FILES_DIR, f"{file_name}.pdf")

    try:
        log_event("PROCESS", f"Checking if file {file_name}.pdf exists for deletion.")

        if not os.path.exists(file_path):
            log_event("ERROR", f"Delete failed: {file_name}.pdf not found.")
            raise HTTPException(status_code=404, detail="File not found.")

        log_event("PROCESS", f"Deleting file: {file_name}.pdf")
        os.remove(file_path)
        log_event("SUCCESS", f"Deleted file: {file_name}.pdf")

        log_event("PROCESS", f"Deleting associated FAISS data for: {file_name}")
        file_delete_pipeline(file_name)
        log_event("SUCCESS", f"Deletion pipeline completed for: {file_name}")

        return {"message": f"{file_name}.pdf and associated data deleted successfully."}

    except Exception as e:
        log_event("ERROR", f"Delete route failed: {e}")
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")
