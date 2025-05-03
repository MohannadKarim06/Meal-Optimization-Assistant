from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pipelines.query_pipeline import query_pipeline

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/ask")
def ask_route(request: QueryRequest):
    try:
        response = query_pipeline(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")
