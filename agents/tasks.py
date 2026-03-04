from crewai import Task
from agents.agents import (
    trend_analyst,
    sentiment_analyst,
    competitor_analyst,
    report_generator
)
from rag.rag_pipeline import retrieve_reviews


def build_tasks(user_query):

    retrieved_reviews = retrieve_reviews(user_query)

    context_text = "\n\n".join([r["text"] for r in retrieved_reviews])

    trend_task = Task(
        description=f"""
        Analyze the following reviews and identify emerging trends:

        {context_text}
        """,
        agent=trend_analyst
    )

    sentiment_task = Task(
        description=f"""
        Analyze sentiment patterns in these reviews:

        {context_text}
        """,
        agent=sentiment_analyst
    )

    competitor_task = Task(
        description=f"""
        Compare brands and identify competitive insights:

        {context_text}
        """,
        agent=competitor_analyst
    )

    report_task = Task(
        description="""
        Combine insights from all analysts and produce structured JSON output:

        {
          "trends": "...",
          "sentiment_summary": "...",
          "competitor_insights": "...",
          "recommendations": "..."
        }
        """,
        agent=report_generator
    )

    return [trend_task, sentiment_task, competitor_task, report_task]