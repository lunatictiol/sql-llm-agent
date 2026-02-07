from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SQL LLM Agent"
    DATABASE_URL: str
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "qwen2.5-7b"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
