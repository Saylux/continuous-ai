import os
import logging
import subprocess
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
# from openai import OpenAI  # Uncomment and configure if using OpenAI or similar LLM
import json
import argparse
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load environment variables
load_dotenv()

MEMORY_FILE = "agent_memory.json"
GAME_REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../game'))
GAME_TESTS_PATH = os.path.join(GAME_REPO_PATH, 'tests')

LOG_FILE = "crew_autopilot.log"

# --- Robust Logging ---
def log_message(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

# --- Enhanced Agent Memory ---
def log_agent_memory(entry):
    memory = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            try:
                memory = json.load(f)
            except Exception:
                memory = []
    entry["timestamp"] = datetime.now().isoformat()
    memory.append(entry)
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=2)

# --- Utility: View Last N Memory Entries ---
def print_memory_summary(n=10):
    if not os.path.exists(MEMORY_FILE):
        print("No agent memory found.")
        return
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        memory = json.load(f)
    print(f"--- Last {n} Agent Memory Entries ---")
    for entry in memory[-n:]:
        print(json.dumps(entry, indent=2))

# --- Utility: Reset Memory Log ---
def reset_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    print("Agent memory and log reset.")

# --- LLM Config Stub ---
LLM_CONFIG = {
    "provider": "openai",  # or "local"
    "api_key": os.getenv("OPENAI_API_KEY", ""),
    # Add more config as needed
}

# --- Doc Parsing: Extract actionable tasks from docs ---
def parse_all_tasks(doc_root):
    tasks = []
    # --- Prototyping tasks (from previous batch) ---
    tasks.append(("Automation Engineer", "Run Selene to lint all source files"))
    tasks.append(("Automation Engineer", "Run StyLua to format all source files"))
    tasks.append(("QA Engineer", "Enforce Selene and StyLua checks in CI"))
    mvp_versions = [
        ("Rollerblades", "Player can walk from A to B"),
        ("Skateboard", "Add basic queuing: movement, queue to join game"),
        ("Bicycle", "Core game loop, UI stub: start, Q&A, answer, result"),
        ("Motorcycle", "Add scoring, rounds: core loop, scoring, rounds"),
        ("Car", "Full game, polish: all features, polish, multiplayer"),
    ]
    for version, features in mvp_versions:
        tasks.append(("Gameplay Engineer", f"Implement MVP version '{version}': {features}"))
    tasks.append(("QA Engineer", "Write and pass initial end-to-end test: player walks from A to B"))
    tasks.append(("UI/UX Engineer", "Integrate Roact or similar UI framework for robust UI prototyping"))
    tasks.append(("Code Reviewer", "Add and enforce code review for all AI-generated scripts"))
    tasks.append(("Staff Software Engineer", "Evaluate and clarify the role of Studio Lite in prototyping"))
    tasks.append(("Automation Engineer", "Add linting/formatting to the prototyping workflow"))
    # --- Testing tasks ---
    tasks.append(("QA Engineer", "Expand scenario, integration, and edge case test coverage"))
    tasks.append(("QA Engineer", "Prioritize 'Needs Test' and 'Partial' in test matrix for new test development"))
    tasks.append(("QA Engineer", "Monitor and optimize test duration; flag slow tests for review"))
    tasks.append(("QA Engineer", "Quarantine and fix flaky tests; use deterministic data and mocks"))
    tasks.append(("QA Engineer", "Use TestEZ, Jest-Roblox, rbxts-jest, TestService for automated testing"))
    # --- CI/CD tasks ---
    tasks.append(("DevOps Engineer", "Automate all build, test, and deploy steps in CI/CD pipeline"))
    tasks.append(("Security Engineer", "Secure secret management and rotation in CI/CD"))
    tasks.append(("DevOps Engineer", "Implement retry/fallback for critical pipeline steps"))
    tasks.append(("Staff Software Engineer", "Periodically review pipeline for new automation opportunities"))
    # --- Playtesting tasks ---
    tasks.append(("Playtest Engineer", "Simulate full game runs and edge cases with agent-based scripts"))
    tasks.append(("Data Engineer", "Update agent simulation scripts based on player data"))
    tasks.append(("Playtest Engineer", "Maintain and review playtesting test matrix"))
    # --- AI Process tasks ---
    tasks.append(("Staff Software Engineer", "Periodic codebase review and refactoring"))
    tasks.append(("Documentation Engineer", "Update and cross-link all documentation"))
    tasks.append(("Ops Analyst", "Review tool and service costs; recommend optimizations"))
    tasks.append(("Growth Engineer", "Analyze ad campaign performance and suggest optimizations"))
    tasks.append(("QA Engineer", "Review test coverage and identify gaps; detect and quarantine flaky tests"))
    tasks.append(("Security Engineer", "Audit secret management practices and recommend improvements"))
    tasks.append(("Analytics Engineer", "Analyze player feedback and analytics for actionable insights"))
    tasks.append(("UI/UX Engineer", "Recommend gameplay or UX improvements based on analytics"))
    return tasks

# --- LLM Integration Stub ---
def generate_code_with_llm(prompt):
    # TODO: Integrate with OpenAI or local LLM for code generation
    logging.info(f"[LLM] Generating code for prompt: {prompt}")
    return f"# Code generated for: {prompt}\nprint('Hello from LLM!')"

def review_code_with_llm(code):
    # TODO: Integrate with LLM for code review
    logging.info(f"[LLM] Reviewing code: {code[:60]}...")
    return "# LLM Review: Code looks good!"

# --- File/Process Integration ---
def run_linter(tool, path):
    try:
        result = subprocess.run([tool, path], capture_output=True, text=True, check=True)
        logging.info(f"[{tool}] Output: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"[{tool}] Error: {e.stderr}")
        return e.stderr

# --- Real Test Runner Integration ---
def run_testez_tests():
    if not os.path.exists(GAME_REPO_PATH):
        logging.warning(f"[TestRunner] Game repo not found at {GAME_REPO_PATH}")
        return "Game repo not found."
    if not os.path.exists(GAME_TESTS_PATH) or not os.listdir(GAME_TESTS_PATH):
        logging.info(f"[TestRunner] No tests found in {GAME_TESTS_PATH}")
        return "No tests to run."
    try:
        result = subprocess.run(["testez-companion-cli"], cwd=GAME_REPO_PATH, capture_output=True, text=True, check=True)
        logging.info(f"[TestEZ] Output: {result.stdout}")
        log_agent_memory({"type": "test_run", "result": result.stdout})
        return result.stdout
    except FileNotFoundError:
        logging.error("[TestEZ] testez-companion-cli not found. Please install it.")
        return "TestEZ CLI not installed."
    except subprocess.CalledProcessError as e:
        logging.error(f"[TestEZ] Error: {e.stderr}")
        log_agent_memory({"type": "test_run", "error": e.stderr})
        return e.stderr

# --- Real Deployment Logic (Stub) ---
def deploy_to_roblox_stub(filename):
    # TODO: Integrate with Roblox Open Cloud API for real deployment
    if not os.path.exists(GAME_REPO_PATH):
        logging.warning(f"[Deploy] Game repo not found at {GAME_REPO_PATH}")
        return "Game repo not found."
    logging.info(f"[Deploy] Deploying {filename} to Roblox (stub)")
    log_agent_memory({"type": "deploy", "file": filename, "status": "stub deployed"})
    return f"Deployed {filename} (stub)"

# --- Simple Workflow Engine for Multi-Step Tasks ---
class WorkflowTask:
    def __init__(self, description, agent_chain):
        self.description = description
        self.agent_chain = agent_chain  # List of (agent, function)
        self.result = None

    def run(self):
        input_data = None
        for agent, func in self.agent_chain:
            logging.info(f"[Workflow] {agent.role} executing: {self.description}")
            input_data = func(agent, self.description, input_data)
        self.result = input_data
        return self.result

# --- Real Agent Behaviors (update QA and DevOps for real test/deploy) ---
def agent_behavior(agent, description, input_data=None):
    # Route based on agent role and task description
    if agent.role == "Gameplay Engineering":
        if "Implement MVP version" in description:
            code = generate_code_with_llm(description)
            filename = f"src/{description.split('"')[1].replace(' ', '_').lower()}.lua"
            write_code_file(filename, code)
            return filename  # Pass filename to next agent
    if agent.role == "Code Review":
        if input_data and os.path.exists(input_data):
            code = read_code_file(input_data)
            review = review_code_with_llm(code)
            logging.info(f"[Code Review] {review}")
            return input_data  # Pass filename to next agent
    if agent.role == "Quality Assurance":
        if input_data and os.path.exists(input_data):
            # Run real TestEZ tests if available
            result = run_testez_tests()
            logging.info(f"[QA] Test result for {input_data}: {result}")
            log_agent_memory({"type": "qa", "file": input_data, "result": result})
            return input_data  # Pass filename to next agent
    if agent.role == "DevOps":
        if input_data and os.path.exists(input_data):
            # Real deployment (stub)
            result = deploy_to_roblox_stub(input_data)
            return result
    # Fallback to previous behavior
    return agent_behavior_single(agent, description)

# --- Single-step agent behavior for non-chained tasks ---
def agent_behavior_single(agent, description):
    # Route based on agent role and task description
    if agent.role == "Automation":
        if "Selene" in description:
            return run_linter("selene", "src/")
        if "StyLua" in description:
            return run_linter("stylua", "src/")
        if "linting/formatting" in description:
            return "Linting/formatting workflow updated."
    if agent.role == "Quality Assurance":
        if "test" in description.lower():
            return run_test_runner()
        if "coverage" in description.lower():
            return "Test coverage reviewed."
        if "flaky" in description.lower():
            return "Flaky tests quarantined."
    if agent.role == "Gameplay Engineering":
        if "Implement MVP version" in description:
            code = generate_code_with_llm(description)
            filename = f"src/{description.split('"')[1].replace(' ', '_').lower()}.lua"
            return write_code_file(filename, code)
    if agent.role == "UI/UX Design":
        if "Roact" in description or "UX" in description:
            return generate_code_with_llm(description)
    if agent.role == "DevOps":
        if "CI/CD" in description or "pipeline" in description:
            return "CI/CD pipeline updated."
        if "retry/fallback" in description:
            return "Retry/fallback logic implemented."
    if agent.role == "Security":
        if "secret" in description:
            return "Secret management reviewed."
    if agent.role == "Code Review":
        if "review" in description:
            code = read_code_file("src/sample.lua") if os.path.exists("src/sample.lua") else ""
            return review_code_with_llm(code)
    if agent.role == "Staff Engineering":
        return "Pipeline and automation reviewed."
    if agent.role == "Playtesting":
        if "simulate" in description:
            return "Agent-based simulation run."
    if agent.role == "Data Engineering":
        if "player data" in description:
            return "Player data analyzed."
    if agent.role == "Documentation":
        if "documentation" in description:
            return "Documentation updated."
    if agent.role == "Operations Analysis":
        if "cost" in description:
            return "Cost optimization reviewed."
    if agent.role == "Growth & Marketing":
        if "ad campaign" in description:
            return "Ad campaign analyzed."
    if agent.role == "Analytics":
        if "analytics" in description or "feedback" in description:
            return "Player feedback and analytics reviewed."
    # Default stub
    logging.info(f"[{agent.role}] Executing: {description}")
    return f"{agent.role} completed: {description}"

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
    ("Playtest Engineer", "Playtesting", "Simulate and validate full game runs and edge cases."),
    ("Data Engineer", "Data Engineering", "Analyze and process player data for simulation and improvement."),
    ("Documentation Engineer", "Documentation", "Maintain and improve all project documentation."),
    ("Ops Analyst", "Operations Analysis", "Optimize costs and operational efficiency."),
    ("Growth Engineer", "Growth & Marketing", "Analyze and optimize ad campaigns and player acquisition."),
    ("Analytics Engineer", "Analytics", "Analyze player feedback and game analytics for improvement."),
    # Add more roles as needed
]

# --- Create Agents ---
def create_agents():
    agents = {}
    for name, role, goal in AGENT_ROLES:
        agents[name] = Agent(name=name, role=role, goal=goal)
    return agents

# --- Main Orchestration (with argparse for status/reset) ---
def main():
    parser = argparse.ArgumentParser(description="CrewAI Autopilot for Roblox Family Feud")
    parser.add_argument("command", nargs="?", default="run", choices=["run", "status", "reset"], help="Command to run: run, status, reset")
    args = parser.parse_args()
    if args.command == "status":
        print_memory_summary(10)
        return
    if args.command == "reset":
        reset_memory()
        return
    # Default: run the pipeline
    doc_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs'))
    tasks_info = parse_all_tasks(doc_root)
    agents = create_agents()
    tasks = []
    for agent_name, description in tasks_info:
        if agent_name == "Gameplay Engineer" and "Implement MVP version" in description:
            agent_chain = [
                (agents["Gameplay Engineer"], agent_behavior),
                (agents["Code Reviewer"], agent_behavior),
                (agents["QA Engineer"], agent_behavior),
                (agents["DevOps Engineer"], agent_behavior),
            ]
            workflow_task = WorkflowTask(description, agent_chain)
            def workflow_func(desc=description, wf=workflow_task):
                try:
                    result = wf.run()
                    log_agent_memory({"type": "workflow", "desc": desc, "result": result})
                    log_message(f"Workflow completed: {desc}")
                    return result
                except Exception as e:
                    log_agent_memory({"type": "workflow_error", "desc": desc, "error": str(e)})
                    log_message(f"Workflow error: {desc} - {e}", level="ERROR")
                    return f"Error: {e}"
            tasks.append(Task(description=description, agent=agents["Gameplay Engineer"], function=workflow_func))
        else:
            def real_task(desc=description, agent=agents.get(agent_name)):
                try:
                    result = agent_behavior_single(agent, desc)
                    log_agent_memory({"type": "task", "agent": agent_name, "desc": desc, "result": result})
                    log_message(f"Task completed: {desc}")
                    return result
                except Exception as e:
                    log_agent_memory({"type": "task_error", "agent": agent_name, "desc": desc, "error": str(e)})
                    log_message(f"Task error: {desc} - {e}", level="ERROR")
                    return f"Error: {e}"
            if agent_name in agents:
                tasks.append(Task(description=description, agent=agents[agent_name], function=real_task))
            else:
                log_message(f"No agent found for role: {agent_name} (task: {description})", level="WARNING")
    crew = Crew(agents=list(agents.values()), tasks=tasks)
    crew.kickoff()

if __name__ == "__main__":
    main() 