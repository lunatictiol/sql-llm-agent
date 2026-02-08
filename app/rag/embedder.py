
from app.rag.qdrant_client import get_vector_store
from app.utils.ids import generate_id
from langchain_core.documents import Document

def embbedDocument(document: list[Document]):
    print("embedding document")
    vector_store = get_vector_store()
    print("adding documents to vector store")
    uuids = [generate_id() for _ in range(len(document))]
    vector_store.add_documents(documents=document,ids=uuids)

    