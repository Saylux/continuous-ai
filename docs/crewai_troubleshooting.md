# CrewAI Troubleshooting & FAQ

## Common Issues

### 1. Installation Problems
- **Error:** `ModuleNotFoundError: No module named 'crewAI'`
  - **Solution:** Run `pip install crewai` in your Python environment.

### 2. Python Version Issues
- **Error:** Syntax errors or unexpected behavior.
  - **Solution:** Ensure you are using Python 3.9 or newer.

### 3. Agent Not Running
- **Error:** Nothing happens when running the script.
  - **Solution:** Check that your `main()` function is called under `if __name__ == "__main__":`.

### 4. Task Fails or Crashes
- **Error:** Exception or error in task function.
  - **Solution:** Add try/except blocks and print/log errors for debugging.

## Debugging Tips
- Use `print()` or Python logging to trace execution.
- Start with a minimal agent and add complexity incrementally.
- Check CrewAI GitHub issues for known bugs.

## FAQ
- **Q:** Can I run multiple agents in parallel?
  - **A:** Yes, CrewAI supports multi-agent orchestration.
- **Q:** How do I integrate with external APIs?
  - **A:** Use Python packages (e.g., `requests`, `PyGithub`) in your agent tasks.
- **Q:** Where can I find more examples?
  - **A:** See the [CrewAI Docs](https://docs.crewai.com/) and [GitHub](https://github.com/joaomdmoura/crewAI). 