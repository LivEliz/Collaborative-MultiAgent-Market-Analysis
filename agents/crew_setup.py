from crewai import Crew, Process
from agents.agents import (
    trend_analyst,
    sentiment_analyst,
    competitor_analyst,
    report_generator
)
from agents.tasks import build_tasks


def create_crew(user_query):
    tasks = build_tasks(user_query)

    crew = Crew(
        agents=[
            trend_analyst,
            sentiment_analyst,
            competitor_analyst,
            report_generator
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        max_iterations=3
    )

    return crew