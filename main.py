import pandas as pd
import json
from transformers import pipeline
from rag_pipeline import RAGPipeline
from agents import data_engineer, retriever, sentiment_analyst, insights_agent
from crewai import Crew, Task

# -----------------------------
# Load reviews from CSV
# -----------------------------
df = pd.read_csv("data/cleaned_reviews.csv")

# Use the 'review_text' column instead of 'review'
reviews = df['review_text'].dropna().tolist()

# -----------------------------
# Initialize RAG pipeline
# -----------------------------
rag = RAGPipeline()
rag.embed_and_store(reviews)

# -----------------------------
# HuggingFace sentiment model
# -----------------------------
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(texts):
    results = sentiment_pipeline(texts)
    pos, neg, neu = 0, 0, 0
    for r in results:
        label = r['label'].lower()
        if "positive" in label:
            pos += 1
        elif "negative" in label:
            neg += 1
        else:
            neu += 1
    total = len(results)
    return {
        "positive": round(pos/total*100, 2),
        "negative": round(neg/total*100, 2),
        "neutral": round(neu/total*100, 2)
    }

# -----------------------------
# Keyword extraction & trends
# -----------------------------
from collections import Counter
import re
import spacy
nlp = spacy.load("en_core_web_sm")

# Basic stopword list (you can expand this)
STOPWORDS = {
    "the","and","for","this","that","with","have","was","are","but","not","you",
    "she","he","they","will","has","had","would","good","great","tablet","amazon"
}

def extract_keywords(context, top_n=5):
    text = " ".join(context).lower()
    doc = nlp(text)
    words = [token.lemma_ for token in doc if token.pos_ in {"NOUN","ADJ"} and token.text not in STOPWORDS]
    common = Counter(words).most_common(top_n)
    return [w for w, _ in common]

def generate_trends(keywords):
    trends = []
    for kw in keywords:
        if "battery" in kw:
            trends.append("Battery life is a recurring concern")
        elif "sound" in kw or "audio" in kw:
            trends.append("Sound quality is highly valued")
        elif "price" in kw or "cost" in kw or "value" in kw:
            trends.append("Affordability influences customer satisfaction")
        elif "quality" in kw:
            trends.append("Build quality is a key factor")
        else:
            trends.append(f"Customers frequently mention {kw}")
    return trends


def generate_recommendations(sentiment, trends):
    recs = []
    if sentiment["negative"] > 30:
        recs.append("Address common complaints in product design")
    if sentiment["positive"] > 50:
        recs.append("Highlight strengths in marketing campaigns")
    for t in trends:
        if "battery" in t:
            recs.append("Invest in improving battery performance")
        elif "sound" in t:
            recs.append("Emphasize sound quality in promotions")
    return recs

# -----------------------------
# Generate structured insights
# -----------------------------
def generate_insights(query, context, sentiment):
    keywords = extract_keywords(context)
    trends = generate_trends(keywords)
    recs = generate_recommendations(sentiment, trends)
    return {
        "query": query,
        "sentiment_summary": sentiment,
        "sample_context": context[:5],  # show first 5 reviews
        "market_trends": trends,
        "recommendations": recs
    }


# -----------------------------
# CrewAI orchestration
# -----------------------------
task_retrieve = Task(
    agent=retriever,
    description="Retrieve relevant reviews",
    expected_output="Relevant product reviews from FAISS index"
)

task_sentiment = Task(
    agent=sentiment_analyst,
    description="Analyze sentiment of retrieved reviews",
    expected_output="Sentiment summary with percentages of positive, negative, neutral"
)

task_insights = Task(
    agent=insights_agent,
    description="Generate market insights",
    expected_output="Structured JSON with trends and actionable recommendations"
)

crew = Crew(
    agents=[data_engineer, retriever, sentiment_analyst, insights_agent],
    tasks=[task_retrieve, task_sentiment, task_insights]
)


crew = Crew(
    agents=[data_engineer, retriever, sentiment_analyst, insights_agent],
    tasks=[task_retrieve, task_sentiment, task_insights]
)

def collaborative_analysis(query):
    context = rag.retrieve(query)
    sentiment = analyze_sentiment(context)
    insights = generate_insights(query, context, sentiment)
    return insights

# -----------------------------
# Run the pipeline
# -----------------------------
if __name__ == "__main__":
    user_query = input("Enter your product query: ")
    result = collaborative_analysis(user_query)
    print(json.dumps(result, indent=2))

