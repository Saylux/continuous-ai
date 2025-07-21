# CrewAI Quickstart Guide

This guide will help you install, configure, and run CrewAI for autonomous agent workflows in the Roblox Family Feud project.

## 1. Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git

## 2. Installation
```bash
pip install crewai
```

## 3. Recommended Project Structure
```
continuous-ai/
└── autonomous_ai_agent/
    ├── agents/
    │   └── my_agent.py
    ├── docs/
    ├── requirements.txt
    └── .env
```
- Place agent scripts in the `agents/` folder.
- Store documentation in `docs/`.
- Use `requirements.txt` for dependencies.
- Use `.env` for secrets and environment variables.

## 4. Environment Management
- Use [virtualenv](https://virtualenv.pypa.io/) or [venv](https://docs.python.org/3/library/venv.html) to isolate dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install crewai
```
- Store secrets (API keys, tokens) in a `.env` file and load them with [python-dotenv](https://pypi.org/project/python-dotenv/).

## 5. Example: Minimal CrewAI Agent
```python
from crewai import Agent, Task, Crew

def main():
    agent = Agent(name="RobloxFeudBot", role="Game Automation", goal="Automate Roblox Family Feud workflows")
    task = Task(description="Sync game code from repo and run tests", agent=agent)
    crew = Crew(agents=[agent], tasks=[task])
    crew.kickoff()

if __name__ == "__main__":
    main()
```

## 6. Running the Agent
```bash
python autonomous_ai_agent/agents/my_agent.py
```

## 7. Debugging Tips
- Use `print()` statements or Python logging for step-by-step output.
- Check CrewAI logs for errors and task results.
- Start with a single agent and task, then expand.

## 8. Key Links
- [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
- [CrewAI Docs](https://docs.crewai.com/) 