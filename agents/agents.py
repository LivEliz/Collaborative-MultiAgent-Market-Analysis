from crewai import Agent, LLM
from rag.rag_pipeline import retrieve_reviews

# -----------------------------
# Ollama LLM Configuration
# -----------------------------
ollama_llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434",
    temperature=0.2
)

# -----------------------------
# Tool Wrapper (Optional Use Later)
# -----------------------------
def rag_tool(query: str):
    return retrieve_reviews(query)

# -----------------------------
# Agents
# -----------------------------

trend_analyst = Agent(
    role="Trend Analyst",
    goal="Extract factual trends from reviews",
    backstory="Expert in identifying observable market trends.",
    verbose=True,
    allow_delegation=False,
    max_iter=2,
    llm=ollama_llm
)

sentiment_analyst = Agent(
    role="Sentiment Analyst",
    goal="Analyze emotional tone in reviews",
    backstory="Expert in NLP and customer psychology.",
    verbose=True,
    allow_delegation=False,
    max_iter=2,
    llm=ollama_llm
)

competitor_analyst = Agent(
    role="Competitor Analyst",
    goal="Compare brands and product positioning",
    backstory="Specialist in competitive intelligence.",
    verbose=True,
    allow_delegation=False,
    max_iter=2,
    llm=ollama_llm
)

report_generator = Agent(
    role="Report Generator",
    goal="Create structured business insights report",
    backstory="Professional business analyst and strategist.",
    verbose=True,
    allow_delegation=False,
    max_iter=2,
    llm=ollama_llm
)