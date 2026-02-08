from typing import Any, Dict
import psycopg


def introspect_schema(connection_string: str) -> Dict[str, Any]:
    """
    Introspect PostgreSQL schema metadata.
    Executes ONLY system catalog queries.
    """

    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:

            # 1. Tables
            cur.execute("""
                SELECT
                    table_schema,
                    table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                  AND table_schema NOT IN ('pg_catalog', 'information_schema')
                ORDER BY table_schema, table_name;
            """)
            tables = cur.fetchall()

            # 2. Columns
            cur.execute("""
                SELECT
                    table_schema,
                    table_name,
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                ORDER BY table_schema, table_name, ordinal_position;
            """)
            columns = cur.fetchall()

            # 3. Primary keys
            cur.execute("""
                SELECT
                    tc.table_schema,
                    tc.table_name,
                    kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                ORDER BY tc.table_schema, tc.table_name;
            """)
            primary_keys = cur.fetchall()

            # 4. Foreign keys
            cur.execute("""
                SELECT
                    tc.table_schema       AS source_schema,
                    tc.table_name         AS source_table,
                    kcu.column_name       AS source_column,
                    ccu.table_schema      AS target_schema,
                    ccu.table_name        AS target_table,
                    ccu.column_name       AS target_column
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                  ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                ORDER BY source_schema, source_table;
            """)
            foreign_keys = cur.fetchall()

            # 5. Indexes
            cur.execute("""
                SELECT
                    schemaname,
                    tablename,
                    indexname,
                    indexdef
                FROM pg_indexes
                WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                ORDER BY schemaname, tablename;
            """)
            indexes = cur.fetchall()

            # 6. Row estimates
            cur.execute("""
                SELECT
                    relname AS table_name,
                    n_live_tup AS estimated_rows
                FROM pg_stat_user_tables
                ORDER BY n_live_tup DESC;
            """)
            row_estimates = cur.fetchall()

    return {
        "tables": [
            {"schema": s, "table": t} for s, t in tables
        ],
        "columns": [
            {
                "schema": s,
                "table": t,
                "column": c,
                "data_type": dt,
                "nullable": n,
                "default": d,
            }
            for s, t, c, dt, n, d in columns
        ],
        "primary_keys": [
            {"schema": s, "table": t, "column": c}
            for s, t, c in primary_keys
        ],
        "foreign_keys": [
            {
                "source_schema": ss,
                "source_table": st,
                "source_column": sc,
                "target_schema": ts,
                "target_table": tt,
                "target_column": tc,
            }
            for ss, st, sc, ts, tt, tc in foreign_keys
        ],
        "indexes": [
            {
                "schema": s,
                "table": t,
                "index": i,
                "definition": d,
            }
            for s, t, i, d in indexes
        ],
        "row_estimates": [
            {"table": t, "estimated_rows": r}
            for t, r in row_estimates
        ],
    }
