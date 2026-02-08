from langchain_core.documents import Document
def normalize_schema_to_text(schema: dict) -> str:
    lines = []

    # --- helpers -------------------------------------------------

    def is_user_table(entry):
        return entry.get("schema") == "public"

    def yn(value):
        return "yes" if value == "YES" else "no"

    # --- collect tables ------------------------------------------

    tables = {
        t["table"]: {
            "schema": t["schema"],
            "columns": [],
            "primary_keys": [],
            "foreign_keys": [],
            "indexes": [],
            "row_estimate": None,
        }
        for t in schema.get("tables", [])
        if is_user_table(t)
    }

    # --- columns -------------------------------------------------

    for col in schema.get("columns", []):
        if col["table"] in tables:
            tables[col["table"]]["columns"].append(col)

    # --- primary keys -------------------------------------------

    for pk in schema.get("primary_keys", []):
        if pk["schema"] == "public" and pk["table"] in tables:
            tables[pk["table"]]["primary_keys"].append(pk["column"])

    # --- foreign keys -------------------------------------------

    for fk in schema.get("foreign_keys", []):
        if fk["source_table"] in tables:
            tables[fk["source_table"]]["foreign_keys"].append(fk)

    # --- indexes ------------------------------------------------

    for idx in schema.get("indexes", []):
        if idx["table"] in tables:
            tables[idx["table"]]["indexes"].append(idx)

    # --- row estimates ------------------------------------------

    for r in schema.get("row_estimates", []):
        if r["table"] in tables:
            tables[r["table"]]["row_estimate"] = r["estimated_rows"]

    # --- render text --------------------------------------------

    for table_name in sorted(tables.keys()):
        t = tables[table_name]

        lines.append(f"Table: {table_name} (schema: {t['schema']})")

        if t["row_estimate"] is not None:
            lines.append(f"Estimated rows: {t['row_estimate']}")

        # Columns
        lines.append("Columns:")
        for c in sorted(t["columns"], key=lambda x: x["column"]):
            col_line = (
                f"- {c['column']}: {c['data_type']}, "
                f"nullable: {yn(c['nullable'])}"
            )
            if c["default"] is not None:
                col_line += f", default: {c['default']}"
            lines.append(col_line)

        # Primary keys
        if t["primary_keys"]:
            lines.append(
                "Primary key: " + ", ".join(sorted(t["primary_keys"]))
            )

        # Foreign keys
        if t["foreign_keys"]:
            lines.append("Foreign keys:")
            for fk in t["foreign_keys"]:
                lines.append(
                    f"- {fk['source_column']} references "
                    f"{fk['target_table']}.{fk['target_column']}"
                )

        # Indexes
        if t["indexes"]:
            lines.append("Indexes:")
            for idx in t["indexes"]:
                lines.append(f"- {idx['index']}")

        lines.append("")  # blank line between tables

    return "\n".join(lines).strip()



def schema_to_documents(schema: dict, schema_id: str) -> list[Document]:
    """
    Convert structured DB schema into semantically meaningful Documents.
    """

    documents: list[Document] = []

    # ---------- TABLES ----------
    for table in schema["tables"]:
        table_name = table["table"]
        table_schema = table["schema"]

        columns = [
            col for col in schema["columns"]
            if col["table"] == table_name
        ]

        column_lines = [
            f"- {c['column']} ({c['data_type']})"
            for c in columns
        ]

        content = f"""
Table: {table_schema}.{table_name}

Columns:
{chr(10).join(column_lines)}
""".strip()

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "schema_id": schema_id,
                    "type": "table",
                    "schema": table_schema,
                    "table": table_name,
                    "columns": [c["column"] for c in columns],
                },
            )
        )

    # ---------- FOREIGN KEYS / RELATIONSHIPS ----------
    for fk in schema["foreign_keys"]:
        content = f"""
Relationship:
{fk['source_schema']}.{fk['source_table']}.{fk['source_column']}
→
{fk['target_schema']}.{fk['target_table']}.{fk['target_column']}
""".strip()

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "schema_id": schema_id,
                    "type": "relationship",
                    "source_table": fk["source_table"],
                    "source_column": fk["source_column"],
                    "target_table": fk["target_table"],
                    "target_column": fk["target_column"],
                },
            )
        )

    # ---------- PRIMARY KEYS ----------
    for pk in schema["primary_keys"]:
        # Ignore system tables defensively
        if pk["schema"] != "public":
            continue

        content = f"""
Primary key:
{pk['schema']}.{pk['table']}.{pk['column']}
""".strip()

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "schema_id": schema_id,
                    "type": "primary_key",
                    "table": pk["table"],
                    "column": pk["column"],
                },
            )
        )

    return documents
