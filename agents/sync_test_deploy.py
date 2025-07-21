import os
import logging
from crewai import Agent, Task, Crew
from github import Github
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME', 'Saylux/roblox-family-feud-game')

# --- Agent Task Functions ---
def sync_code():
    try:
        logging.info('Syncing code from GitHub...')
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        # Example: list files in repo root
        contents = repo.get_contents("")
        for content_file in contents:
            logging.info(f"Found file: {content_file.path}")
        return "Code sync complete"
    except Exception as e:
        logging.error(f"Sync error: {e}")
        return f"Sync failed: {e}"

def run_tests():
    try:
        logging.info('Running tests (stub)...')
        # Insert test runner logic here (e.g., subprocess to run pytest, TestEZ, etc.)
        # For now, simulate success
        return "Tests passed"
    except Exception as e:
        logging.error(f"Test error: {e}")
        return f"Test failed: {e}"

def deploy_game():
    try:
        logging.info('Deploying game (stub)...')
        # Insert deployment logic here (e.g., call Roblox Open Cloud API)
        # For now, simulate success
        return "Game deployed"
    except Exception as e:
        logging.error(f"Deploy error: {e}")
        return f"Deploy failed: {e}"

# --- CrewAI Agents ---
sync_agent = Agent(name="SyncBot", role="Sync", goal="Sync code from GitHub repo")
test_agent = Agent(name="TestBot", role="Test", goal="Run all tests")
deploy_agent = Agent(name="DeployBot", role="Deploy", goal="Deploy game to Roblox")

# --- CrewAI Tasks ---
task1 = Task(description="Sync code", agent=sync_agent, function=sync_code)
task2 = Task(description="Run tests", agent=test_agent, function=run_tests)
task3 = Task(description="Deploy game", agent=deploy_agent, function=deploy_game)

# --- Orchestrate Workflow ---
def main():
    crew = Crew(agents=[sync_agent, test_agent, deploy_agent], tasks=[task1, task2, task3])
    crew.kickoff()

if __name__ == "__main__":
    main() 