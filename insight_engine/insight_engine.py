import plotly.graph_objects as go
from collections import Counter
import re


def generate_insights(data):
    """
    Converts CrewAI agent JSON output into:
    - Metrics
    - SWOT
    - Plotly charts
    for Streamlit dashboard
    """

    # ---------------------------------
    # Extract fields safely
    # ---------------------------------
    trends = data.get("trends", [])
    sentiment = data.get("sentiment_summary", {})
    competitors = data.get("competitor_insights", [])
    recommendations = data.get("recommendations", [])

    # ---------------------------------
    # FIX: Ensure trends is always a list
    # ---------------------------------
    if isinstance(trends, dict):
        trends = list(trends.values())
    elif isinstance(trends, set):
        trends = list(trends)
    elif isinstance(trends, str):
        trends = [trends]
    elif trends is None:
        trends = []

    # ---------------------------------
    # FIX: Flatten nested lists
    # ---------------------------------
    flat_trends = []
    for t in trends:
        if isinstance(t, list):
            flat_trends.extend([str(x) for x in t])
        else:
            flat_trends.append(str(t))

    trends = flat_trends

    # ---------------------------------
    # Convert sentiment to integers
    # ---------------------------------
    def safe_int(value):
        try:
            return int(value)
        except:
            return 0

    positive = safe_int(sentiment.get("positive"))
    negative = safe_int(sentiment.get("negative"))
    neutral = safe_int(sentiment.get("neutral"))

    total = positive + negative + neutral

    # ---------------------------------
    # Trend Score
    # ---------------------------------
    if total > 0:
        trend_score = round(((positive - negative) / total) * 100)
    else:
        trend_score = 0

    # ---------------------------------
    # Sentiment Donut Chart
    # ---------------------------------
    fig_sentiment = go.Figure(
        data=[
            go.Pie(
                labels=["Positive", "Negative", "Neutral"],
                values=[positive, negative, neutral],
                hole=0.65,
                textinfo="percent",
                marker=dict(
                    colors=["#a8e6cf", "#ffb6b9", "#dcedc1"],
                    line=dict(color="white", width=3),
                ),
            )
        ]
    )

    fig_sentiment.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text=f"<b>{total}</b><br>Reviews",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=28),
            )
        ],
    )

    # ---------------------------------
    # Keyword Frequency Chart
    # ---------------------------------
    fig_keywords = None

    if trends:

        combined_text = " ".join(trends).lower()

        # remove punctuation
        combined_text = re.sub(r"[^\w\s]", "", combined_text)

        stopwords = {
            "the", "is", "a", "to", "and", "for", "of", "on",
            "with", "this", "that", "was", "are", "very"
        }

        words = [
            w for w in combined_text.split()
            if w not in stopwords and len(w) > 3
        ]

        if words:

            freq = Counter(words).most_common(8)

            labels = [x[0] for x in freq]
            values = [x[1] for x in freq]

            fig_keywords = go.Figure(
                data=[
                    go.Bar(
                        x=labels,
                        y=values,
                        text=values,
                        textposition="outside",
                        marker=dict(
                            color=values,
                            colorscale="Blues"
                        )
                    )
                ]
            )

            fig_keywords.update_layout(
                margin=dict(t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=True),
            )

    # ---------------------------------
    # SWOT Analysis
    # ---------------------------------
    half = max(1, len(trends) // 2)

    strengths = trends[:half] if trends else ["Positive customer feedback"]
    weaknesses = trends[half:] if len(trends) > 1 else ["Minor usability issues"]

    opportunities = recommendations if recommendations else [
        "Improve product differentiation"
    ]

    threats = []
    for c in competitors:
        if isinstance(c, dict) and "brand" in c:
            threats.append(c["brand"])

    if not threats:
        threats = ["Low-cost competitors entering market"]

    swot = {
        "Strengths": strengths,
        "Weaknesses": weaknesses,
        "Opportunities": opportunities,
        "Threats": threats,
    }

    # ---------------------------------
    # Risk Detection
    # ---------------------------------
    risk_alert = None

    if negative > positive:
        risk_alert = "Negative sentiment exceeding positive feedback."

    if negative >= 5:
        risk_alert = "Critical issue detected: High negative sentiment spike."

    # ---------------------------------
    # Market Position Summary
    # ---------------------------------
    market_position = (
        f"Trend Score: {trend_score}/100 | "
        f"Competitors Mentioned: {len(competitors)}"
    )

    # ---------------------------------
    # Return structured insights
    # ---------------------------------
    return {
        "trend_score": trend_score,
        "swot_analysis": swot,
        "market_positioning": market_position,
        "risk_alert": risk_alert,
        "charts": {
            "sentiment": fig_sentiment,
            "keywords": fig_keywords
        }
    }