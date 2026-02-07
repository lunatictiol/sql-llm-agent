from fastapi import APIRouter

router = APIRouter()

@router.post("/query")
async def execute_query(nl_query: str):
    # Placeholder for NL -> SQL logic
    return {"sql": "SELECT * FROM placeholder", "result": []}
