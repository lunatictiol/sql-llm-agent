from sqlalchemy import create_engine, inspect

def introspect_schema(database_url: str):
    engine = create_engine(database_url)
    inspector = inspect(engine)
    schema = {}
    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({"name": column["name"], "type": str(column["type"])})
        schema[table_name] = columns
    return schema
