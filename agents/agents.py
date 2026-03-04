from crewai import Agent
from rag.rag_pipeline import retrieve_reviews

# Tool wrapper for RAG
def rag_tool(query: str):
    return retrieve_reviews(query)

trend_analyst = Agent(
    role="Trend Analyst",
    goal="Identify emerging product trends from reviews",
    backstory="Expert in market research and consumer behavior.",
    verbose=True,
    allow_delegation=False
)

sentiment_analyst = Agent(
    role="Sentiment Analyst",
    goal="Analyze emotional tone and satisfaction patterns",
    backstory="Expert in NLP and customer psychology.",
    verbose=True,
    allow_delegation=False
)

competitor_analyst = Agent(
    role="Competitor Analyst",
    goal="Compare brands and product positioning",
    backstory="Specialist in competitive intelligence.",
    verbose=True,
    allow_delegation=False
)

report_generator = Agent(
    role="Report Generator",
    goal="Create structured business insights report",
    backstory="Professional business analyst and strategist.",
    verbose=True,
    allow_delegation=False
)