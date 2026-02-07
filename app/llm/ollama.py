from langchain_ollama import ChatOllama
from pathlib import Path


def load_prompt(name: str) -> str:
    return Path(f"app/llm/prompts/{name}.txt").read_text()

def build_llm():
    return ChatOllama(
        model="qwen2.5-coder",
        temperature=0.1,
    )
