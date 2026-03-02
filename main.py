# ==============================================
# STEP 1: IMPORT LIBRARIES
# ==============================================

import pandas as pd
import numpy as np
import os


# ==============================================
# STEP 2: LOAD DATASET
# ==============================================

# Make sure amazon_raw.csv is in the same folder as this script
file_path = "amazon_raw.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(
        "amazon_raw.csv not found. Please download the dataset manually and place it in this folder."
    )

df = pd.read_csv(file_path)

print("\nDataset Loaded Successfully!")
print(df.head())
print("\nDataset Info:")
print(df.info())


# ==============================================
# STEP 3: DATA CLEANING & PREPROCESSING
# ==============================================

print("\nCleaning dataset...")

# Clean and extract required columns
df["review_text"] = df["reviews.text"].fillna("").astype(str).str.lower()
df["product_name"] = df["name"].fillna("Unknown Product")
df["rating"] = pd.to_numeric(df["reviews.rating"], errors="coerce").fillna(0)
df["date"] = pd.to_datetime(df["reviews.date"], errors="coerce").dt.strftime("%Y-%m-%d")
df["category"] = df["categories"].str.split(",").str[0].fillna("Unknown")

# Select required columns
cleaned_df = df[
    ["review_text", "product_name", "rating", "date", "category"]
].copy()

print(f"\nCleaned dataset shape: {cleaned_df.shape}")
print("\nFirst few rows:")
print(cleaned_df.head())

print("\nMissing values:")
print(cleaned_df.isnull().sum())


# ==============================================
# STEP 4: SAVE CLEANED DATASET
# ==============================================

output_file = "cleaned_reviews.csv"
cleaned_df.to_csv(output_file, index=False)

print("\n✅ cleaned_reviews.csv saved successfully!")
print("\nDataset Summary:")
print(f"- Total reviews: {len(cleaned_df)}")
print(f"- Categories: {cleaned_df['category'].nunique()}")
print(f"- Rating range: {cleaned_df['rating'].min()} - {cleaned_df['rating'].max()}")


# ==============================================
# END OF SCRIPT
# ==============================================

print("\n🚀 Data preprocessing completed successfully!")