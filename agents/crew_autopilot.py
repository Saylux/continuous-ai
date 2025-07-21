import os
import logging
import subprocess
from dotenv import load_dotenv
import json
from datetime import datetime
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load environment variables
load_dotenv()

MEMORY_FILE = "agent_memory.json"
LOG_FILE = "crew_autopilot.log"

# --- Robust Logging ---
def log_message(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

# --- LLM Integration: Gemini Support ---
def generate_code_with_llm(prompt):
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        log_message(f"[LLM] No GEMINI_API_KEY found. Returning stub code for: {prompt}", level="WARNING")
        return f"# [LLM STUB] Code generated for: {prompt}\nprint('Hello from LLM stub!')"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def review_code_with_llm(code):
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        log_message(f"[LLM] No GEMINI_API_KEY found. Returning stub review.", level="WARNING")
        return "# [LLM STUB] Review: Code looks fine (stub)."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Review this code:\n{code}")
    return response.text

# --- File/Process Integration ---
def write_code_file(filename, code):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)
    log_message(f"[FileIO] Wrote code to {filename}")
    return f"Wrote code to {filename}"

def read_code_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    log_message(f"[FileIO] Read code from {filename}")
    return code

def run_testez_tests():
    # Stub: always pass
    log_message("[TestRunner] (Stub) All tests passed.")
    return "All tests passed (stub)"

def deploy_to_roblox_stub(filename):
    log_message(f"[Deploy] (Stub) Deployed {filename} to Roblox.")
    return f"Deployed {filename} (stub)"

# --- Agent Roles and Workflow ---
MVP_VERSIONS = [
    ("Rollerblades", "Player can walk from A to B"),
    ("Skateboard", "Add basic queuing: movement, queue to join game"),
    ("Bicycle", "Core game loop, UI stub: start, Q&A, answer, result"),
    ("Motorcycle", "Add scoring, rounds: core loop, scoring, rounds"),
    ("Car", "Full game, polish: all features, polish, multiplayer"),
]

def main():
    log_message("Starting Gemini-based CrewAI workflow (no CrewAI dependencies)...")
    for version, features in MVP_VERSIONS:
        desc = f'Implement MVP version "{version}": {features}'
        # 1. Gameplay Engineer: Generate code
        code = generate_code_with_llm(desc)
        filename = f"src/{version.replace(' ', '_').lower()}.lua"
        write_code_file(filename, code)
        # 2. Code Reviewer: Review code
        review = review_code_with_llm(code)
        log_message(f"[Review] {review}")
        # 3. QA Engineer: Test code
        test_result = run_testez_tests()
        log_message(f"[QA] {test_result}")
        # 4. DevOps Engineer: Deploy code
        deploy_result = deploy_to_roblox_stub(filename)
        log_message(f"[DevOps] {deploy_result}")
        # Log memory
        with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "version": version,
                "desc": desc,
                "file": filename,
                "review": review,
                "test_result": test_result,
                "deploy_result": deploy_result
            }) + "\n")
    log_message("Workflow complete.")

if __name__ == "__main__":
    main() 