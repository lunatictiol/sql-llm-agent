from fastapi import FastAPI
# from app.core.config import settings
# from app.api import router as api_router

app = FastAPI(
    title="SQL LLM Agent",
    description="FastAPI based LLM agent with RAG, MCP, and SQL capabilities",
    version="0.1.0",
)

# app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to SQL LLM Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
