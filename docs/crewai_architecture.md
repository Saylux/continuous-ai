# CrewAI Architecture for Roblox Family Feud Automation

```mermaid
graph TD
    subgraph CrewAI System
        Agent1["Agent: SyncBot"]
        Agent2["Agent: TestBot"]
        Agent3["Agent: DeployBot"]
        Task1["Task: Sync Code"]
        Task2["Task: Run Tests"]
        Task3["Task: Deploy Game"]
        Crew["Crew (Orchestrator)"]
    end
    Crew --> Agent1
    Crew --> Agent2
    Crew --> Agent3
    Agent1 --> Task1
    Agent2 --> Task2
    Agent3 --> Task3
```

## Explanation
- **Agents**: Each agent is responsible for a specific automation role (e.g., syncing code, running tests, deploying).
- **Tasks**: Tasks are assigned to agents and define the work to be done.
- **Crew**: The Crew object orchestrates the workflow, assigning tasks to agents and managing execution order.

This modular design allows you to add, remove, or modify agents and tasks as your automation needs evolve. 