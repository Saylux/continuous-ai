import os
import sys
import subprocess
import platform

def run(cmd, shell=False):
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=shell, check=False)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def generate_env_file():
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("GEMINI_API_KEY=\n")
        print("Created .env with GEMINI_API_KEY=")

def ensure_requirements():
    if not os.path.exists("requirements.txt"):
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write("crewai\npython-dotenv\ngoogle-generativeai\n")
        print("Created requirements.txt")

def main():
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    import argparse
    parser = argparse.ArgumentParser(description="CrewAI Autopilot runner")
    parser.add_argument("command", nargs="?", default="run", choices=["run", "list-models"], help="Command to run: run, list-models")
    args = parser.parse_args()

    # Ensure all required files exist
    generate_env_file()
    ensure_requirements()
    
    venv_dir = "venv"
    is_windows = platform.system() == "Windows"

    # 1. Create virtual environment if it doesn't exist
    if not os.path.isdir(venv_dir):
        print("Creating virtual environment...")
        run([sys.executable, "-m", "venv", venv_dir])

    # 2. Construct the path to the Python executable in the venv
    if is_windows:
        python_bin = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_bin = os.path.join(venv_dir, "Scripts", "pip.exe")
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:
        python_bin = os.path.join(venv_dir, "bin", "python")
        pip_bin = os.path.join(venv_dir, "bin", "pip")
        activate_script = os.path.join(venv_dir, "bin", "activate")

    # 3. If not already running in venv, re-invoke self in venv
    if os.path.abspath(sys.executable) != os.path.abspath(python_bin):
        # Install/upgrade all dependencies
        run([pip_bin, "install", "--upgrade", "pip"])
        run([pip_bin, "install", "-r", "requirements.txt"])
        run([pip_bin, "install", "--upgrade", "google-generativeai"])
        run([pip_bin, "install", "python-dotenv"])
        
        # Re-run this script using the venv Python
        new_env = os.environ.copy()
        if is_windows:
            run([python_bin, os.path.abspath(__file__), args.command])
        else:
            new_env["PATH"] = os.path.dirname(python_bin) + os.pathsep + new_env.get("PATH", "")
            run(["/bin/bash", "-c", f"source {activate_script} && {python_bin} {os.path.abspath(__file__)} {args.command}"], shell=True, env=new_env)
        sys.exit(0)

    # 4. Now in venv: load .env if needed
    from dotenv import load_dotenv
    load_dotenv()

    if not os.environ.get('OPENAI_API_KEY'):
        os.environ['OPENAI_API_KEY'] = 'dummy'

    if args.command == "list-models":
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
            print("\nAvailable Gemini models:")
            for model in genai.list_models():
                print(f"- {model.name}")
        except Exception as e:
            print(f"\nError listing models: {str(e)}")
        return

    # 5. Run the CrewAI autopilot script
    autopilot_script = os.path.join("agents", "crew_autopilot.py")
    run([python_bin, autopilot_script])

if __name__ == "__main__":
    main() 