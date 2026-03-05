import json
import matplotlib.pyplot as plt
from collections import Counter

# -----------------------------
# Load Agent Output
# -----------------------------
with open("insight_engine/agent_output.json") as f:
    data = json.load(f)

trends = data["trends"]
sentiment = data["sentiment_summary"]
competitors = data["competitor_insights"]
recommendations = data["recommendations"]

# Convert sentiment strings to integers
positive = int(sentiment["positive"])
negative = int(sentiment["negative"])
neutral = int(sentiment["neutral"])

# -----------------------------
# Trend Score Calculation
# -----------------------------
trend_score = positive - negative

# -----------------------------
# Sentiment Distribution Chart
# -----------------------------
labels = ["Positive", "Negative", "Neutral"]
values = [positive, negative, neutral]

plt.bar(labels, values)
plt.title("Customer Sentiment Distribution")
plt.ylabel("Review Count")
plt.savefig("charts/sentiment_chart.png")
plt.close()

# -----------------------------
# Keyword Frequency Analysis
# -----------------------------
all_text = " ".join(trends)
words = all_text.split()

freq = Counter(words)

plt.bar(freq.keys(), freq.values())
plt.title("Keyword Frequency in Trends")
plt.xticks(rotation=45)
plt.savefig("charts/keyword_chart.png")
plt.close()

# -----------------------------
# SWOT Analysis
# -----------------------------
swot = {
    "Strengths": trends[:2],
    "Weaknesses": trends[2:4],
    "Opportunities": recommendations,
    "Threats": [c["brand"] for c in competitors]
}

# -----------------------------
# Market Positioning Summary
# -----------------------------
market_position = f"""
Trend Score: {trend_score}

Competitors Detected: {len(competitors)}

Positive Sentiment: {positive}
Negative Sentiment: {negative}
"""

# -----------------------------
# Risk Alert
# -----------------------------
risk_alert = None

if negative > positive:
    risk_alert = "High negative sentiment detected"

# -----------------------------
# Recommendation Engine
# -----------------------------
def recommendation_engine():

    if negative > 3:
        return "Urgent product improvement required"

    elif positive > 5:
        return "Expand marketing and product line"

    else:
        return "Monitor market trends"

recommendation_result = recommendation_engine()

# -----------------------------
# Final Business Report
# -----------------------------
final_report = {
    "trend_score": trend_score,
    "swot_analysis": swot,
    "market_positioning": market_position,
    "risk_alert": risk_alert,
    "recommendation_engine": recommendation_result
}

with open("final_report.json", "w") as f:
    json.dump(final_report, f, indent=4)

print("Insight Engine Completed")
