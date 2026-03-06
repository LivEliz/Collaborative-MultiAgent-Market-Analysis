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
CHUNK_SIZE = 120
TOP_K_MULTIPLIER = 5

# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# ============================================================
# CHUNKING FUNCTION
# ============================================================

def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = str(text).split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

# ============================================================
# BUILD FAISS INDEX
# ============================================================

def build_index():

    print("Building FAISS index...")

    df = pd.read_csv(DATA_PATH)

    documents = []
    metadata = []

    for _, row in df.iterrows():

        # Use rag_text for better semantic embedding
        base_text = str(row["rag_text"])

        chunks = chunk_text(base_text)

        for chunk in chunks:

            documents.append(chunk)

            metadata.append({
                "text": chunk,
                "product_name": row["product_name"],
                "category": row["category"],
                "rating": row["rating"],
                "price": row["price"],
                "review_title": row["review_title"],
                "helpful_votes": row["helpful_votes"],
                "recommended": row["recommended"],
                "review_date": row["review_date"]
            })

    if len(documents) == 0:
        raise ValueError("No documents available for indexing.")

    embeddings = model.encode(documents, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("FAISS index built successfully")

    return index, metadata

# ============================================================
# LOAD EXISTING INDEX
# ============================================================

def load_index():

    print("Loading FAISS index...")

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
# REVIEW RETRIEVAL
# ============================================================

def retrieve_reviews(
        query: str,
        top_k: int = 5,
        min_rating: float = None,
        category: str = None
):

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, top_k * TOP_K_MULTIPLIER)

    results = []
    seen = set()

    for idx in indices[0]:

        if idx < 0:
            continue

        item = metadata[idx]

        if item["text"] in seen:
            continue

        if min_rating is not None and item["rating"] < min_rating:
            continue

        if category is not None and category.lower() not in str(item["category"]).lower():
            continue

        results.append(item)
        seen.add(item["text"])

        if len(results) >= top_k:
            break

    return results

# ============================================================
# CONTEXT BUILDER FOR CREWAI
# ============================================================

def get_context_for_agents(query: str):

    results = retrieve_reviews(query, top_k=5)

    context_blocks = []

    for i, r in enumerate(results, 1):

        block = f"""
---------------- REVIEW {i} ----------------

Product Name: {r['product_name']}
Category: {r['category']}
Price: {r['price']}
Rating: {r['rating']}
Review Title: {r['review_title']}
Helpful Votes: {r['helpful_votes']}
Recommended: {r['recommended']}

Customer Review:
{r['text']}

-------------------------------------------
"""

        context_blocks.append(block)

    context = "\n".join(context_blocks)

    return context