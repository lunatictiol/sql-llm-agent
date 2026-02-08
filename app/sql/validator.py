import json
from pathlib import Path

from langchain_ollama import ChatOllama
from app.sql.errors import SQLValidationError
from app.llm.utils import load_prompt,strip_markdown
from app.llm.models import ModelType

def validate_sql_with_llm(
    *,
    sql: str,
    schema_context: str,
    user_question: str,
) -> None:
    """
    Uses Phi-3 to validate SQL against schema context.
    Raises SQLValidationError if invalid.
    """

    prompt_template = load_prompt("sql_validator")
    print("sql",sql)

    prompt = [
        {
            "role": "system",
            "content": prompt_template
        },
        {
            "role": "user",
            "content": f"""
            schema context: {schema_context}
            sql: {sql}
            user question: {user_question}
            """
        }
    ]
    llm = ChatOllama(
        model=ModelType.PHI,
        temperature=0.0,  # CRITICAL for validation
    )

    response = llm.invoke(prompt)
    print("response",response.content)
    content = strip_markdown(response.content)
    print("content",content)

    # # 🔒 HARD SAFETY: ensure string
    # if not isinstance(response, str):
    #     raise SQLValidationError(
    #         f"Validator returned non-text response: {type(response)}"
    #     )

    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        raise SQLValidationError(
            f"Validator returned invalid JSON: {response}"
        )

    if not isinstance(result, dict):
        raise SQLValidationError("Validator response is not a JSON object")

    if result.get("valid") is not True:
        raise SQLValidationError(
            result.get("reason", "SQL validation failed")
        )
