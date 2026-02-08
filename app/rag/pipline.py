from app.rag.schema_loader import load_schema    
from app.rag.embedder import embbedDocument    
from app.rag.documents import schema_to_documents,normalize_schema_to_text
from app.utils.ids import generate_id

from app.core.redis import redis_client
def store_schema_document(connection_string: str):
    print("generating id")
    schema_id=generate_id()
    print("loading schema")
    schema = load_schema(connection_string)
    print("normalizing schema")
    schema_documents = schema_to_documents(schema,schema_id)
    print("storing schema in redis")
    schema_text=normalize_schema_to_text(schema)
    redis_client.setex(
    name=f"schema:{schema_id}",
    time=86400,  # 1 day
    value=schema_text
    ) 
    print("embedding schema")
    embbedDocument(document=schema_documents)
    print("schema stored successfully")
    return schema_id
    