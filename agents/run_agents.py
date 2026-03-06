from agents.crew_setup import create_crew
import json
import os


if __name__ == "__main__":

    user_query = input("Enter market analysis query: ")

    crew = create_crew(user_query)

    result = crew.kickoff()

    print("\nFINAL OUTPUT:\n")

    # CrewAI returns CrewOutput object
    final_output = result.raw

    print(final_output)

    # Convert JSON string to dictionary safely
    try:
        output_json = json.loads(final_output)
    except:
        output_json = {"raw_output": final_output}

    # Ensure directory exists
    os.makedirs("insight_engine", exist_ok=True)

    # Save output
    with open("insight_engine/agent_output.json", "w") as f:
        json.dump(output_json, f, indent=4)

    print("\nOutput saved to insight_engine/agent_output.json")