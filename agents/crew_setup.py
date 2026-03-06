from crewai import Crew, Process

from agents.agents import (
    trend_analyst,
    sentiment_analyst,
    competitor_analyst,
    report_generator
)

from agents.tasks import build_tasks


def create_crew(user_query):

    # Build tasks dynamically
    tasks = build_tasks(user_query)

    # Create Crew
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
        memory=False,
        cache=False,
        full_output=True
    )

    return crew