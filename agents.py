from crewai import Agent

# Use Ollama as the LLM provider
ollama_model = "ollama/llama3.2:3b"  # or "ollama/mistral"

data_engineer = Agent(
    role="Data Engineer",
    goal="Preprocess product reviews for analysis",
    backstory="Expert in cleaning and structuring raw review data.",
    llm=ollama_model
)

retriever = Agent(
    role="Retriever",
    goal="Fetch relevant context using FAISS",
    backstory="Specialist in information retrieval.",
    llm=ollama_model
)

sentiment_analyst = Agent(
    role="Sentiment Analyst",
    goal="Analyze sentiment trends in reviews",
    backstory="Understands customer emotions and opinions.",
    llm=ollama_model
)

insights_agent = Agent(
    role="Market Insights",
    goal="Generate structured insights from context and sentiment",
    backstory="Translates analysis into actionable recommendations.",
    llm=ollama_model
)
