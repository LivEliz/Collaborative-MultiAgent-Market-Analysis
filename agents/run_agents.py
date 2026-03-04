from agents.crew_setup import create_crew

if __name__ == "__main__":

    user_query = input("Enter market analysis query: ")

    crew = create_crew(user_query)

    result = crew.kickoff()

    print("\n\nFINAL OUTPUT:\n")
    print(result)