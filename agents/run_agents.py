from agents.crew_setup import create_crew
import json

if __name__ == "__main__":

    user_query = input("Enter market analysis query: ")

    crew = create_crew(user_query)

    result = crew.kickoff()

    print("\n\nFINAL OUTPUT:\n")
    print(result)

    # Save output for Insight Engine
    with open("insight_engine/agent_output.json", "w") as f:
        json.dump(result, f, indent=4)
