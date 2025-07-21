from crewai import Agent, Task, Crew

def sync_and_test():
    try:
        print("Syncing code...")
        # Simulate code sync
        print("Running tests...")
        # Simulate test run
        return "Success"
    except Exception as e:
        print(f"Error: {e}")
        return "Failed"

if __name__ == "__main__":
    agent = Agent(name="SyncBot", role="Sync & Test", goal="Keep code up to date and tested")
    task = Task(description="Sync and test code", agent=agent, function=sync_and_test)
    crew = Crew(agents=[agent], tasks=[task])
    crew.kickoff() 