from rag.rag_pipeline import retrieve_reviews

results = retrieve_reviews(
    query="battery life and reading experience",
    top_k=5
)

for r in results:
    print("\nProduct:", r["product_name"])
    print("Rating:", r["rating"])
    print("Review:", r["text"])