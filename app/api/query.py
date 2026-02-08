from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.pipline import store_schema_document

router = APIRouter()

class SchemaRequest(BaseModel):
    url: str


    
@router.post("/schema")
def store_schema(req: SchemaRequest):
    try:
        schema_id=store_schema_document(req.url)
        return {
            "message": "Schema stored successfully",
            "schema_id": schema_id,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

