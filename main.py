# ==============================================
# STEP 1: IMPORT LIBRARIES
# ==============================================

import pandas as pd
import numpy as np
import os
import json


# ==============================================
# STEP 2: LOAD DATASET
# ==============================================

file_path = os.path.join("data", "amazon_raw.csv")

if not os.path.exists(file_path):
    raise FileNotFoundError(
        "amazon_raw.csv not found. Please place the dataset in this folder."
    )

df = pd.read_csv(file_path)

print("\nDataset Loaded Successfully")
print("Shape:", df.shape)


# ==============================================
# STEP 3: HELPER FUNCTION TO EXTRACT PRICE
# ==============================================

def extract_price(price_json):
    try:
        prices = json.loads(price_json.replace("'", '"'))
        if isinstance(prices, list) and len(prices) > 0:
            return prices[0].get("amountMax", None)
    except:
        return None
    return None


# ==============================================
# STEP 4: DATA CLEANING
# ==============================================

print("\nCleaning dataset...")

# Keep original text
df["review_text"] = df["reviews.text"].fillna("").astype(str)

# Review title
df["review_title"] = df["reviews.title"].fillna("").astype(str)

# Product name
df["product_name"] = df["name"].fillna("Unknown Product")

# Rating
df["rating"] = pd.to_numeric(df["reviews.rating"], errors="coerce")

# Helpful votes
df["helpful_votes"] = pd.to_numeric(df["reviews.numHelpful"], errors="coerce").fillna(0)

# Recommendation flag
df["recommended"] = df["reviews.doRecommend"].fillna(False)

# Date
df["review_date"] = pd.to_datetime(df["reviews.date"], errors="coerce")

# User location
df["user_city"] = df["reviews.userCity"].fillna("Unknown")
df["user_province"] = df["reviews.userProvince"].fillna("Unknown")

# Username
df["username"] = df["reviews.username"].fillna("Anonymous")

# Category
df["category"] = df["categories"].str.split(",").str[0].fillna("Unknown")

# Extract price
df["price"] = df["prices"].apply(lambda x: extract_price(str(x)))

# Weight
df["weight"] = df["weight"].fillna("Unknown")

# UPC
df["upc"] = df["upc"].fillna("Unknown")


# ==============================================
# STEP 5: REMOVE USELESS ROWS
# ==============================================

# Remove rows with empty review text
df = df[df["review_text"].str.strip() != ""]

# Remove duplicates
df = df.drop_duplicates(subset=["review_text"])

print("After cleaning shape:", df.shape)


# ==============================================
# STEP 6: CREATE TEXT FIELD FOR RAG
# ==============================================

# Combine fields for embedding context
df["rag_text"] = (
    "Product: " + df["product_name"] +
    ". Rating: " + df["rating"].astype(str) +
    ". Title: " + df["review_title"] +
    ". Review: " + df["review_text"]
)


# ==============================================
# STEP 7: SELECT IMPORTANT COLUMNS
# ==============================================

cleaned_df = df[
    [
        "product_name",
        "category",
        "price",
        "rating",
        "review_title",
        "review_text",
        "rag_text",
        "helpful_votes",
        "recommended",
        "review_date",
        "user_city",
        "user_province",
        "username",
        "weight",
        "upc"
    ]
]


# ==============================================
# STEP 8: SAVE CLEAN DATASET
# ==============================================

output_file = "cleaned_reviews.csv"

cleaned_df.to_csv(output_file, index=False)

print("\ncleaned_reviews.csv saved successfully")


# ==============================================
# STEP 9: DATA SUMMARY
# ==============================================

print("\nDataset Summary")
print("Total reviews:", len(cleaned_df))
print("Products:", cleaned_df["product_name"].nunique())
print("Categories:", cleaned_df["category"].nunique())
print("Average rating:", cleaned_df["rating"].mean())
print("Price range:", cleaned_df["price"].min(), "-", cleaned_df["price"].max())


print("\nData preprocessing completed")