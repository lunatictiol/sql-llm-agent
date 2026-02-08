import sqlparse


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
    "COPY",
    "CALL",
    "VACUUM",
    "ANALYZE",
}


def validate_sql_ast_with_reason(sql: str) -> tuple[bool, str]:
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False, "No SQL statement found."
    if len(parsed) != 1:
        return False, "Multiple SQL statements are not allowed."

    stmt = parsed[0]
    if stmt.get_type().upper() != "SELECT":
        return False, "Only SELECT statements are allowed."

    for token in stmt.flatten():
        value = token.value.upper()
        if value in FORBIDDEN_KEYWORDS:
            return False, f"Forbidden keyword detected: {value}."

    return True, "OK"


def validate_sql_ast(sql: str) -> bool:
    ok, _ = validate_sql_ast_with_reason(sql)
    return ok
