import os
import logging
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load environment variables
load_dotenv()

# --- Doc Parsing: Extract actionable tasks from docs ---
def parse_prototyping_tasks(doc_root):
    tasks = []
    # Linting/Formatting tasks
    tasks.append(("Automation Engineer", "Run Selene to lint all source files"))
    tasks.append(("Automation Engineer", "Run StyLua to format all source files"))
    tasks.append(("QA Engineer", "Enforce Selene and StyLua checks in CI"))
    # MVP/Transitionary game tasks
    mvp_versions = [
        ("Rollerblades", "Player can walk from A to B"),
        ("Skateboard", "Add basic queuing: movement, queue to join game"),
        ("Bicycle", "Core game loop, UI stub: start, Q&A, answer, result"),
        ("Motorcycle", "Add scoring, rounds: core loop, scoring, rounds"),
        ("Car", "Full game, polish: all features, polish, multiplayer"),
    ]
    for version, features in mvp_versions:
        tasks.append(("Gameplay Engineer", f"Implement MVP version '{version}': {features}"))
    # End-to-end test
    tasks.append(("QA Engineer", "Write and pass initial end-to-end test: player walks from A to B"))
    # Tooling/Improvement tasks
    tasks.append(("UI/UX Engineer", "Integrate Roact or similar UI framework for robust UI prototyping"))
    tasks.append(("Code Reviewer", "Add and enforce code review for all AI-generated scripts"))
    tasks.append(("Staff Software Engineer", "Evaluate and clarify the role of Studio Lite in prototyping"))
    tasks.append(("Automation Engineer", "Add linting/formatting to the prototyping workflow"))
    return tasks

# --- Define Agent Roles (expanded) ---
AGENT_ROLES = [
    ("Product Manager", "Product Management", "Turn requirements into actionable user stories and tasks."),
    ("Architect", "System Architecture", "Design robust, scalable systems for Roblox Family Feud."),
    ("Frontend Engineer", "Frontend Development", "Build engaging Roblox UIs and user experiences."),
    ("Backend Engineer", "Backend Development", "Implement game logic, APIs, and data storage."),
    ("Gameplay Engineer", "Gameplay Engineering", "Implement core game mechanics and features."),
    ("QA Engineer", "Quality Assurance", "Test and validate all game features and code."),
    ("DevOps Engineer", "DevOps", "Automate builds, tests, and deployments for Roblox."),
    ("UI/UX Engineer", "UI/UX Design", "Design user flows, wireframes, and interfaces."),
    ("Security Engineer", "Security", "Ensure security best practices in code and infra."),
    ("Automation Engineer", "Automation", "Automate repetitive tasks, linting, formatting, and CI checks."),
    ("Code Reviewer", "Code Review", "Review code and docs for quality and correctness."),
    ("Staff Software Engineer", "Staff Engineering", "Lead technical improvements and evaluate new tools."),
    # Add more roles as needed
]

# --- Create Agents ---
def create_agents():
    agents = {}
    for name, role, goal in AGENT_ROLES:
        agents[name] = Agent(name=name, role=role, goal=goal)
    return agents

# --- Main Orchestration ---
def main():
    doc_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs'))
    tasks_info = parse_prototyping_tasks(doc_root)
    agents = create_agents()
    tasks = []
    for agent_name, description in tasks_info:
        agent = agents.get(agent_name)
        if agent:
            def stub_task(desc=description, agent=agent_name):
                logging.info(f"[{agent}] Executing: {desc}")
                return f"{agent} completed: {desc}"
            tasks.append(Task(description=description, agent=agent, function=stub_task))
        else:
            logging.warning(f"No agent found for role: {agent_name} (task: {description})")
    crew = Crew(agents=list(agents.values()), tasks=tasks)
    crew.kickoff()

if __name__ == "__main__":
    main() 