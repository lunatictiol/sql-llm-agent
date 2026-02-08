from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.query import router as query_router
app = FastAPI(
    title="SQL LLM Agent",
    description="FastAPI based LLM agent with RAG, MCP, and SQL capabilities",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Welcome to SQL LLM Agent API"}

app.include_router(chat_router,prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(query_router, prefix="/api/v1")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
