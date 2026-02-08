from pathlib import Path
from langchain_core.messages import AIMessage

def load_prompt(name: str) -> str: return Path(f"app/llm/prompts/{name}.txt").read_text()

def strip_markdown(text: str) -> str:
    if text.startswith("```"):
        text = text.split("```")[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    if text.startswith("json"):
        text = text.split("json")[1]    
    return text.strip()


def extract_ai_content(response: AIMessage) -> str:
    messages = response.get("messages", [])

    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            return strip_markdown(msg.content)

    raise ValueError("No AIMessage found in response")