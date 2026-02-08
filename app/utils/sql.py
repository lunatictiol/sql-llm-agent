def format_sql(sql: str) -> str:
    return sql.strip()


def extract_sql(text: str) -> str:
    cleaned = text.strip()
    if "```" in cleaned:
        parts = cleaned.split("```")
        if len(parts) >= 2:
            cleaned = parts[1]
            if cleaned.lstrip().lower().startswith("sql"):
                cleaned = cleaned.lstrip()[3:]
    cleaned = cleaned.strip()
    if cleaned.lower().startswith("sql:"):
        cleaned = cleaned[4:].strip()
    return cleaned
