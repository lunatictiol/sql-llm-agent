from app.db.introspection import introspect_schema

def load_schema(db_connection):
    try:
        return introspect_schema(db_connection)
    except Exception as e:
        raise e
