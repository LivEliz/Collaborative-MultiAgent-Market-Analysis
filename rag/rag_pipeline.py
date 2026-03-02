# ============================================================
# PRODUCTION RAG PIPELINE
# Member 2 – RAG Engineer
# ============================================================

import os
import pickle
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_reviews.csv")
RAG_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(RAG_DIR, "faiss_index.index")
METADATA_PATH = os.path.join(RAG_DIR, "metadata.pkl")


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 200


# ============================================================
# LOAD MODEL (Only once)
# ============================================================

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)


# ============================================================
# CHUNKING FUNCTION
# ============================================================

def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


# ============================================================
# BUILD INDEX (ONLY IF NOT EXISTS)
# ============================================================

def build_index():
    print("Building FAISS index from scratch...")

    df = pd.read_csv(DATA_PATH)

    documents = []
    metadata = []

    for _, row in df.iterrows():
        chunks = chunk_text(str(row["review_text"]))

        for chunk in chunks:
            documents.append(chunk)
            metadata.append({
                "text": chunk,
                "product_name": row["product_name"],
                "rating": row["rating"],
                "category": row["category"],
                "date": row["date"]
            })

    embeddings = model.encode(documents, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("Index built and saved successfully!")

    return index, metadata


# ============================================================
# LOAD EXISTING INDEX
# ============================================================

def load_index():
    print("Loading existing FAISS index...")
    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


# ============================================================
# INITIALIZE SYSTEM
# ============================================================

if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
    index, metadata = load_index()
else:
    index, metadata = build_index()


# ============================================================
# MAIN RETRIEVAL FUNCTION (CrewAI Ready)
# ============================================================

def retrieve_reviews(
    query: str,
    top_k: int = 5,
    min_rating: float = None,
    category: str = None
):
    """
    Retrieve relevant review chunks with optional metadata filtering.

    Parameters:
        query (str): User search query
        top_k (int): Number of results to return
        min_rating (float): Filter by minimum rating
        category (str): Filter by category

    Returns:
        List[dict]: Retrieved results with metadata
    """

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k * 3)

    results = []

    for idx in indices[0]:
        item = metadata[idx]

        if min_rating is not None and item["rating"] < min_rating:
            continue

        if category is not None and category.lower() not in str(item["category"]).lower():
            continue

        results.append(item)

        if len(results) >= top_k:
            break

    return results


# ============================================================
# CREWAI INTEGRATION FUNCTION
# ============================================================

def get_context_for_agents(query: str) -> str:
    """
    Returns formatted context string for LLM agents.
    """

    results = retrieve_reviews(query, top_k=5)

    context = "\n\n".join(
        [f"Product: {r['product_name']}\nRating: {r['rating']}\nReview: {r['text']}"
         for r in results]
    )

    return context


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":
    user_query = input("\nEnter your search query: ")

    results = retrieve_reviews(user_query)

    print("\nTop Results:\n")
    for r in results:
        print(r)
        print("-" * 80)