from app.llm.base import BaseLLM

class LLMSQLValidator:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def validate(self, sql: str, schema: dict) -> bool:
        # Construct prompt and ask LLM
        return True
