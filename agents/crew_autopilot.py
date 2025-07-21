import os
import logging
import subprocess
from dotenv import load_dotenv
import json
from datetime import datetime
import requests
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load environment variables
load_dotenv()

MEMORY_FILE = "agent_memory.json"
LOG_FILE = "crew_autopilot.log"
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Robust Logging ---
def log_message(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

def call_gemini_api(prompt: str) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        log_message("[LLM] No GEMINI_API_KEY found.", level="WARNING")
        return None

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }

    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    try:
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract the generated text from the response
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']
            if 'parts' in content and content['parts']:
                return content['parts'][0]['text']
        
        return None
    except Exception as e:
        log_message(f"[LLM] Error calling Gemini API: {str(e)}", level="ERROR")
        return None

def generate_code_with_llm(prompt: str) -> str:
    code = call_gemini_api(f"""
    Generate Lua code for Roblox game development task:
    {prompt}
    
    Requirements:
    - Use Roblox Lua APIs
    - Include error handling
    - Add comments explaining the code
    - Make it modular and reusable
    """)
    
    if code is None:
        log_message(f"[LLM] Failed to generate code for: {prompt}", level="WARNING")
        return f"-- [STUB] Failed to generate code for: {prompt}\nprint('Hello from stub!')"
    
    return code

def review_code_with_llm(code: str) -> str:
    review = call_gemini_api(f"""
    Review this Roblox Lua code:
    
    {code}
    
    Provide a code review that covers:
    - Code quality and style
    - Potential bugs or issues
    - Performance considerations
    - Security concerns
    - Suggestions for improvement
    """)
    
    if review is None:
        log_message("[LLM] Failed to review code", level="WARNING")
        return "-- [STUB] Code review failed. Please review manually."
    
    return review

# --- File/Process Integration ---
def write_code_file(filename: str, code: str) -> str:
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)
        log_message(f"[FileIO] Wrote code to {filename}")
        return f"Wrote code to {filename}"
    except Exception as e:
        log_message(f"[FileIO] Error writing to {filename}: {str(e)}", level="ERROR")
        return f"Failed to write to {filename}: {str(e)}"

def read_code_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        log_message(f"[FileIO] Read code from {filename}")
        return code
    except Exception as e:
        log_message(f"[FileIO] Error reading {filename}: {str(e)}", level="ERROR")
        return f"Failed to read {filename}: {str(e)}"

def run_testez_tests() -> str:
    # Stub: always pass
    log_message("[TestRunner] (Stub) All tests passed.")
    return "All tests passed (stub)"

def deploy_to_roblox_stub(filename: str) -> str:
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
    log_message("Starting Gemini-based workflow (using Gemini 2.0 Flash)...")
    try:
        for version, features in MVP_VERSIONS:
            desc = f'Implement MVP version "{version}": {features}'
            # 1. Gameplay Engineer: Generate code
            code = generate_code_with_llm(desc)
            filename = f"src/{version.lower().replace(' ', '_')}.lua"
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
            try:
                with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({
                        "version": version,
                        "desc": desc,
                        "file": filename,
                        "review": review,
                        "test_result": test_result,
                        "deploy_result": deploy_result
                    }) + "\n")
            except Exception as e:
                log_message(f"[Memory] Error writing to memory file: {str(e)}", level="ERROR")
        log_message("Workflow complete.")
    except Exception as e:
        log_message(f"[Main] Critical error in workflow: {str(e)}", level="ERROR")
        raise

if __name__ == "__main__":
    main() 