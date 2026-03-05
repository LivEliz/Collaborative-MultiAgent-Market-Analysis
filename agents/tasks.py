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

    # Remove duplicate reviews
    unique_reviews = list({r["text"]: r for r in retrieved_reviews}.values())
    context_text = "\n\n".join([r["text"] for r in unique_reviews])

    # ==========================
    # STEP 1 — Trend Analysis
    # ==========================
    trend_task = Task(
        description=f"""
    Extract ONLY observable trends from the reviews.

    STRICT RULES:
    - Use ONLY the reviews provided.
    - Do NOT use external knowledge.
    - Identify:
      - Product strengths
      - Product weaknesses
      - Recurring issues
      - Pricing/value perceptions
      - Customer satisfaction patterns
    - If no trend exists, return empty list.
    - No explanations.
    - No extra text.

    Return result in STRICT JSON format:

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
        expected_output="Structured JSON trends.",
        output_format="json",
        agent=trend_analyst
    )

    # ==========================
    # STEP 2 — Sentiment Analysis
    # ==========================
    sentiment_task = Task(
        description="""
Based ONLY on the trends generated.

Return sentiment counts in STRICT JSON format.

Return exactly this structure:

{
  "positive": "count",
  "negative": "count",
  "neutral": "count"
}

example:
positive: 5
negative: 1
neutral: 2

Rules:
- No explanations.
- No markdown.
- Return JSON only.
""",
        expected_output="Valid sentiment JSON.",
        agent=sentiment_analyst,
        context=[trend_task]
    )

    # ==========================
    # STEP 3 — Competitor Analysis
    # ==========================
    competitor_task = Task(
        description="""
Based ONLY on trends.

Extract competitor insights.

STRICT RULES:
- Include only explicitly mentioned brands.
- Do NOT invent brands.
- If none mentioned, return empty list [].
- No speculation.
- Return JSON format.

Return structure:

[
  {
    "brand": "",
    "insight": ""
  }
]
""",
        expected_output="Valid competitor JSON list.",
        agent=competitor_analyst,
        context=[trend_task]
    )

    # ==========================
    # STEP 4 — Final Report
    # ==========================
    report_task = Task(
        description="""
Generate FINAL REPORT in STRICT VALID JSON.

VERY IMPORTANT:
- Return ONLY JSON.
- No markdown.
- No explanations.
- No extra text.
- Double quotes only.
- Must match schema exactly.
- Generate 2–4 actionable business recommendations based strictly on trends and sentiment.

If any section has no data, return empty list or empty strings.

FINAL SCHEMA:

{
  "trends": [],
  "sentiment_summary": {
    "positive": "",
    "negative": "",
    "neutral": ""
  },
  "competitor_insights": [],
  "recommendations": []
}
""",
        expected_output="Strict valid JSON only.",
        output_format="json",
        agent=report_generator,
        context=[trend_task, sentiment_task, competitor_task]
    )

    return [trend_task, sentiment_task, competitor_task, report_task]