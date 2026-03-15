from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGPipeline:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def embed_and_store(self, texts):
        embeddings = self.model.encode(texts)
        self.index.add(embeddings)
        self.texts.extend(texts)

    def retrieve(self, query, k=5):
        query_vec = self.model.encode([query])
        distances, indices = self.index.search(query_vec, k)
        return [self.texts[i] for i in indices[0]]
