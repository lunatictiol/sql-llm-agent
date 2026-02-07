from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    mode: str
    message: str


@router.post("/chat")
def chat(req: ChatRequest):
    # TODO: Implement actual query logic
    result = "Query mode logic placeholder" 
    return {"response": result}
