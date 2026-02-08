import dspy
from app.sql.errors import SQLValidationError
from app.llm.models import ModelType


# -------------------------
# 1. Signature (the contract)
# -------------------------

class SQLValidationSignature(dspy.Signature):
    """
    Validate SQL legality against schema (not business semantics).
    """

    schema_context: str = dspy.InputField(
        desc="Authoritative database schema"
    )
    sql: str = dspy.InputField(
        desc="SQL query to validate"
    )
    user_question: str = dspy.InputField(
        desc="User question (for contradiction check only)"
    )

    valid: bool = dspy.OutputField(
        desc="True if SQL is valid"
    )
    reason: str = dspy.OutputField(
        desc="Short explanation"
    )


# -------------------------
# 2. Validator module
# -------------------------

class SQLValidator(dspy.Module):
    def forward(self, schema_context: str, sql: str, user_question: str):
        return dspy.Predict(SQLValidationSignature)(
            schema_context=schema_context,
            sql=sql,
            user_question=user_question,
        )


# -------------------------
# 3. Public API (what you call)
# -------------------------

def validate_sql_with_llm(
    *,
    sql: str,
    schema_context: str,
    user_question: str,
) -> None:
    """
    Uses Phi-3 + DSPy to validate SQL.
    Raises SQLValidationError if invalid.
    """

    # Configure Phi-3 for DSPy (deterministic)
    phi3 = dspy.LM('ollama_chat/phi3', api_base='http://localhost:11434', api_key='')

    dspy.configure(lm=phi3)

    validator = SQLValidator()

    result = validator(
        schema_context=schema_context,
        sql=sql,
        user_question=user_question,
    )

    # DSPy guarantees structure here
    if result.valid is not True:
        raise SQLValidationError(result.reason)
