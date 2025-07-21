# CrewAI Advanced Examples

## 1. Multi-Agent Orchestration
```python
from crewai import Agent, Task, Crew

def sync_code():
    print("Syncing code...")
    return "Code synced"

def run_tests():
    print("Running tests...")
    return "Tests passed"

def deploy_game():
    print("Deploying game...")
    return "Game deployed"

sync_agent = Agent(name="SyncBot", role="Sync", goal="Sync code from repo")
test_agent = Agent(name="TestBot", role="Test", goal="Run all tests")
deploy_agent = Agent(name="DeployBot", role="Deploy", goal="Deploy game to Roblox")

task1 = Task(description="Sync code", agent=sync_agent, function=sync_code)
task2 = Task(description="Run tests", agent=test_agent, function=run_tests)
task3 = Task(description="Deploy game", agent=deploy_agent, function=deploy_game)

crew = Crew(agents=[sync_agent, test_agent, deploy_agent], tasks=[task1, task2, task3])
crew.kickoff()
```

## 2. Integrating with External APIs (e.g., GitHub)
```python
import os
from crewai import Agent, Task, Crew
from github import Github  # pip install PyGithub

def list_repos():
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)
    for repo in g.get_user().get_repos():
        print(repo.name)
    return "Repos listed"

github_agent = Agent(name="GitHubBot", role="GitHub Integration", goal="List all repos for user")
task = Task(description="List GitHub repos", agent=github_agent, function=list_repos)
crew = Crew(agents=[github_agent], tasks=[task])
crew.kickoff()
```

## 3. Error Handling and Notifications
```python
import smtplib
from crewai import Agent, Task, Crew

def notify_error():
    try:
        # Simulate error
        raise Exception("Something went wrong!")
    except Exception as e:
        print(f"Error: {e}")
        # Send email or log error
        return "Error notified"

notify_agent = Agent(name="NotifyBot", role="Notifier", goal="Notify on errors")
task = Task(description="Notify on error", agent=notify_agent, function=notify_error)
crew = Crew(agents=[notify_agent], tasks=[task])
crew.kickoff()
``` 