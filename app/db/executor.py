import psycopg


def execute_safe_query(query: str, conn, timeout_ms: int):
    with psycopg.connect(
        host=conn.host,
        port=conn.port,
        dbname=conn.database,
        user=conn.user,
        password=conn.password,
        options=f"-c statement_timeout={timeout_ms}",
    ) as connection:
        with connection.cursor() as cur:
            cur.execute(query)
            cols = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(cols, row)) for row in rows]
