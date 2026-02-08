from langchain_ollama import OllamaEmbeddings

class Embeddings:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model="embeddinggemma",
        )
    def embed_query(self, query: str):
        return self.embeddings.embed_query(query)

