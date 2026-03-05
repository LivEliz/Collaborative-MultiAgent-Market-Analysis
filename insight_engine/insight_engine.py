import plotly.graph_objects as go
import plotly.express as px
from collections import Counter

def generate_insights(data):
    """
    Takes the structured JSON output from the CrewAI agents and returns 
    processed insights and Plotly chart objects for the Streamlit frontend.
    """
    trends = data.get("trends", [])
    sentiment = data.get("sentiment_summary", {"positive": 0, "negative": 0, "neutral": 0})
    competitors = data.get("competitor_insights", [])
    recommendations = data.get("recommendations", [])

    # Convert sentiment to integers safely
    try:
        positive = int(sentiment.get("positive", 0))
    except ValueError:
        positive = 0
    try:
        negative = int(sentiment.get("negative", 0))
    except ValueError:
        negative = 0
    try:
        neutral = int(sentiment.get("neutral", 0))
    except ValueError:
        neutral = 0

    # -----------------------------
    # Trend Score Calculation
    # -----------------------------
    # Normalize between -100 to 100 based on total
    total = positive + negative + neutral
    if total > 0:
        trend_score = round(((positive - negative) / total) * 100)
    else:
        trend_score = 0

    # -----------------------------
    # Sentiment Donut Chart (Plotly)
    # -----------------------------
    labels = ["Positive", "Negative", "Neutral"]
    values = [positive, negative, neutral]
    colors = ["#a8e6cf", "#ffb6b9", "#dcedc1"]  # Soft Pastel Mint, Pink, Pale Green

    fig_sentiment = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.65,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=4)),
        textinfo='percent',
        hoverinfo='label+percent+value',
        textfont=dict(color='#475569', family='Outfit', size=14)
    )])
    
    fig_sentiment.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text=f'<b>{total}</b><br><span style="font-size:12px;color:#94a3b8;">REVIEWS</span>', x=0.5, y=0.5, font_size=32, showarrow=False, font_color='#475569', font_family='Outfit')]
    )

    # -----------------------------
    # Keyword Frequency Chart (Plotly)
    # -----------------------------
    fig_keywords = None
    if trends:
        all_text = " ".join(trends).lower()
        stopwords = {'the', 'a', 'to', 'and', 'is', 'in', 'it', 'for', 'of', 'on', 'with', 'this', 'that', 'are', 'was', 'as', 'at', 'be', 'but', 'not'}
        words = [w for w in all_text.split() if w not in stopwords and len(w) > 3]
        
        if words:
            freq = Counter(words).most_common(8)
            kw_labels = [item[0] for item in freq]
            kw_values = [item[1] for item in freq]
            
            fig_keywords = go.Figure(data=[go.Bar(
                x=kw_labels,
                y=kw_values,
                marker=dict(
                    color=kw_values,
                    colorscale=[[0, '#add8e6'], [1, '#ffb6c1']], # Pastel Blue to Pastel Pink Gradient
                ),
                marker_line_width=0,
                opacity=0.9,
                text=kw_values,
                textposition='outside',
                textfont=dict(color='#475569', family='Outfit', size=13)
            )])
            
            fig_keywords.update_layout(
                margin=dict(t=30, b=20, l=0, r=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#475569', family='Outfit'),
                xaxis=dict(showgrid=False, linecolor='rgba(0,0,0,0.1)', tickfont=dict(size=12)),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', linecolor='rgba(0,0,0,0)', showticklabels=False),
            )

    # -----------------------------
    # SWOT Analysis Grid
    # -----------------------------
    swot = {
        "Strengths": trends[:max(1, len(trends)//2)] if trends else ["Consistent reliability noted"],
        "Weaknesses": trends[max(1, len(trends)//2):] if len(trends) > 1 else ["Some connectivity issues mentioned"],
        "Opportunities": recommendations if recommendations else ["Expand product ecosystem integration"],
        "Threats": [c["brand"] for c in competitors] if competitors else ["Emerging budget-friendly alternatives"]
    }

    # -----------------------------
    # Market Positioning & Rick Alerts
    # -----------------------------
    market_position = f"Score: {trend_score}/100 | Detected {len(competitors)} major competitors in context."
    risk_alert = "High negative sentiment spike detected!" if negative > positive else None

    # -----------------------------
    # Return structured insights for frontend
    # -----------------------------
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
