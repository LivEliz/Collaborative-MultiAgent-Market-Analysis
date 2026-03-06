from crewai import Task
from agents.agents import (
    trend_analyst,
    sentiment_analyst,
    competitor_analyst,
    report_generator
)
from rag.rag_pipeline import retrieve_reviews


def build_tasks(user_query):

    # ==========================
    # Retrieve Reviews (RAG)
    # ==========================
    retrieved_reviews = retrieve_reviews(user_query)

    unique_reviews = list({r["text"]: r for r in retrieved_reviews}.values())

    context_text = "\n\n".join([
        f"""
Product: {r['product_name']}
Rating: {r['rating']}

Review:
{r['text']}
"""
        for r in unique_reviews
    ])

    # ==========================
    # STEP 1 — Trend Analysis
    # ==========================
    trend_task = Task(
        description=f"""
Analyze the following product reviews and extract observable trends.

Use ONLY the information present in the reviews.

Identify:

1. Product strengths
2. Product weaknesses
3. Recurring issues mentioned by multiple customers
4. Pricing or value perceptions
5. Customer satisfaction patterns

Rules:
- Do NOT add outside knowledge
- Extract short factual points
- Each point must be under 12 words
- If no data exists for a section return empty list

Return ONLY valid JSON using this schema:

{{
  "strengths": [],
  "weaknesses": [],
  "recurring_issues": [],
  "pricing_perception": [],
  "customer_satisfaction_patterns": []
}}

USER QUERY:
{user_query}

REVIEWS:
{context_text}
""",
        expected_output="Valid JSON containing trend categories.",
        output_format="json",
        agent=trend_analyst
    )

    # ==========================
    # STEP 2 — Sentiment Analysis
    # ==========================
    sentiment_task = Task(
        description="""
Analyze the trends extracted from reviews and determine overall sentiment.

Rules:
- Count positive observations
- Count negative observations
- Count neutral observations
- Return numeric values

Return ONLY valid JSON:

{
  "positive": 0,
  "negative": 0,
  "neutral": 0
}
""",
        expected_output="Valid sentiment JSON with numeric values.",
        output_format="json",
        agent=sentiment_analyst,
        context=[trend_task]
    )

    # ==========================
    # STEP 3 — Competitor Analysis
    # ==========================
    competitor_task = Task(
        description="""
Identify competitor brands explicitly mentioned in the reviews.

Rules:
- Only include brands directly mentioned in reviews
- Do NOT infer competitors
- If none mentioned return empty list

Return JSON format:

[
  {
    "brand": "",
    "insight": ""
  }
]
""",
        expected_output="List of competitor insights in JSON.",
        output_format="json",
        agent=competitor_analyst,
        context=[trend_task]
    )

    # ==========================
    # STEP 4 — Final Report
    # ==========================
    report_task = Task(
        description="""
Generate the final structured business insights report.

Use outputs from:
- Trend analysis
- Sentiment analysis
- Competitor analysis

Rules:
- Return ONLY JSON
- No markdown
- No explanations
- Generate 2–4 actionable recommendations

Schema must match exactly:

{
  "trends": {
    "strengths": [],
    "weaknesses": [],
    "recurring_issues": [],
    "pricing_perception": [],
    "customer_satisfaction_patterns": []
  },
  "sentiment_summary": {
    "positive": 0,
    "negative": 0,
    "neutral": 0
  },
  "competitor_insights": [],
  "recommendations": []
}
""",
        expected_output="Final structured report JSON.",
        output_format="json",
        agent=report_generator,
        context=[trend_task, sentiment_task, competitor_task]
    )

    return [
        trend_task,
        sentiment_task,
        competitor_task,
        report_task
    ]