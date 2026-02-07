from sqlalchemy import create_engine, text

def execute_sql(database_url: str, sql: str):
    engine = create_engine(database_url)
    with engine.connect() as connection:
        result = connection.execute(text(sql))
        return [dict(row) for row in result]
