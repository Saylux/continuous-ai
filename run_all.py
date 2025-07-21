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

def main():
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
    else:
        python_bin = os.path.join(venv_dir, "bin", "python")
        pip_bin = os.path.join(venv_dir, "bin", "pip")

    # 3. Upgrade pip and install requirements
    run([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    run([pip_bin, "install", "-r", "requirements.txt"])

    # 4. Run the CrewAI autopilot script
    autopilot_script = os.path.join("agents", "crew_autopilot.py")
    run([python_bin, autopilot_script])

if __name__ == "__main__":
    main() 