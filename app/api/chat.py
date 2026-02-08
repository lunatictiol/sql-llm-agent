from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.orchestrator.query_pipline import run_query_pipeline
router = APIRouter()
class QueryRequest(BaseModel):
    question: str
    schema_id: str


@router.post("/chat")
def generate_sql(req: QueryRequest):
    return run_query_pipeline(req.question,req.schema_id)
