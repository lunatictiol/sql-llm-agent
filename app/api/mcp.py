from fastapi import APIRouter

router = APIRouter()

@router.get("/tools")
async def list_tools():
    # Placeholder for listing MCP tools
    return {"tools": []}
