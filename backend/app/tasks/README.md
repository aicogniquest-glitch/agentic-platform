# ADK Agent Tasks

This directory contains task definitions converted from GitHub issues into a format compatible with Google's Agent Development Kit (ADK).

## Overview

The pending GitHub issues have been converted into structured agent tasks that can be executed by ADK agents. Each task includes:

- **Task Definition**: Structured information about what needs to be done
- **Agent Assignment**: Recommended ADK agent for executing the task
- **Acceptance Criteria**: Clear success metrics
- **Dependencies**: Task execution order
- **Subtasks**: Breakdown of work items

## Task Structure

Each `AgentTask` contains:

```python
@dataclass
class AgentTask:
    task_id: str                    # Unique identifier (e.g., "task_0001")
    title: str                      # Task title
    description: str                # Detailed description
    instruction: str                # Operational goal for the agent
    acceptance_criteria: List[str]  # Success criteria
    complexity: TaskComplexity      # small, medium, or large
    labels: List[str]               # Category labels
    tools_required: List[str]       # Required tools/technologies
    dependencies: List[str]         # Dependent task IDs
    status: TaskStatus              # pending, in_progress, completed, failed
    github_issue_number: int        # Original GitHub issue number
    estimated_hours: float          # Time estimate
    subtasks: List[str]             # Breakdown of work
```

## Available Tasks

### Task 0001: Develop execution panel and monitoring dashboard
- **Complexity**: Large (40 hours)
- **Agent**: FrontendDeveloperAgent
- **GitHub Issue**: #1
- **Status**: Pending
- Build React components for live execution monitoring and analytics dashboard

### Task 0002: Create ADK configuration module
- **Complexity**: Medium (8 hours)
- **Agent**: ConfigurationAgent
- **GitHub Issue**: #2
- **Status**: Pending
- Implement configuration management for environment variables and ADK settings

### Task 0003: Implement React frontend with Agent, Tool, and Workflow Builders
- **Complexity**: Large (60 hours)
- **Agent**: FrontendDeveloperAgent
- **GitHub Issue**: #3
- **Status**: Pending
- **Dependencies**: task_0002
- Create visual builder interface for agents, tools, and workflows

### Task 0004: Build backend service layer for business logic
- **Complexity**: Medium (24 hours)
- **Agent**: BackendDeveloperAgent
- **GitHub Issue**: #4
- **Status**: Pending
- **Dependencies**: task_0002
- Develop service layer architecture for business logic

**Total Estimated Effort**: 132 hours

## Recommended Execution Order

Based on dependencies, execute tasks in this order:

1. `task_0001` - Execution panel (no dependencies)
2. `task_0002` - Configuration module (no dependencies)
3. `task_0003` - React builders (depends on task_0002)
4. `task_0004` - Backend services (depends on task_0002)

## Using the Task CLI

A command-line interface is provided to interact with tasks:

### List all tasks
```bash
python task_cli.py list
```

### Filter by status
```bash
python task_cli.py list --status pending
```

### Filter by complexity
```bash
python task_cli.py list --complexity large
```

### Show detailed task information
```bash
python task_cli.py show task_0002
```

### View task statistics
```bash
python task_cli.py stats
```

### Show dependency order
```bash
python task_cli.py dependency-order
```

### Export tasks to JSON
```bash
python task_cli.py export --output tasks.json
```

### Export task-agent mapping
```bash
python task_cli.py export-mapping --output mapping.json
```

## Agent Definitions

Four specialized agents are defined to handle different task types:

### FrontendDeveloperAgent
- **Model**: gemini-2.5-pro
- **Specializes in**: React, Material-UI, ReactFlow, WebSocket integration
- **Handles**: Frontend development, UI/UX, dashboards

### BackendDeveloperAgent
- **Model**: gemini-2.5-pro
- **Specializes in**: Python, FastAPI, SQLAlchemy, ADK integration
- **Handles**: Service layer, APIs, database, business logic

### ConfigurationAgent
- **Model**: gemini-2.5-pro
- **Specializes in**: Pydantic Settings, environment management
- **Handles**: Configuration, settings, environment variables

### FullStackAgent
- **Model**: gemini-2.5-pro
- **Specializes in**: Full-stack development
- **Handles**: End-to-end features, integration work

## Integration with ADK

These task definitions follow Google ADK's structure:

```python
# Example of how an ADK agent would consume a task
from app.tasks.task_manager import get_task_manager

manager = get_task_manager()
task = manager.get_task("task_0002")

# Get the recommended agent for the task
agent_info = manager.get_task_with_agent("task_0002")

# Create an ADK agent (pseudo-code)
agent = Agent(
    name=agent_info["agent"]["name"],
    model=agent_info["agent"]["model"],
    instruction=task.instruction,
    tools=task.tools_required,
)

# Execute the task
result = agent.execute()
```

## Task Status Management

Update task status as work progresses:

```python
from app.tasks.task_manager import get_task_manager
from app.tasks.task_definitions import TaskStatus

manager = get_task_manager()

# Mark task as in progress
manager.update_task_status("task_0002", TaskStatus.IN_PROGRESS)

# Mark task as completed
manager.update_task_status("task_0002", TaskStatus.COMPLETED)
```

## File Structure

```
backend/app/
├── tasks/
│   ├── __init__.py
│   ├── task_definitions.py    # Task data structures and definitions
│   └── task_manager.py        # Task management functionality
├── agents/
│   ├── __init__.py
│   └── agent_definitions.py   # ADK agent configurations
└── config/
    └── (to be created by task_0002)

backend/
├── task_cli.py                # Command-line interface
├── tasks.json                 # Exported tasks (generated)
└── task_agent_mapping.json   # Task-agent mapping (generated)
```

## Next Steps

1. Review the task definitions and agent assignments
2. Adjust priorities or dependencies if needed
3. Set up the ADK environment with required models
4. Execute tasks in dependency order
5. Update task status as work progresses
6. Track progress and metrics using the CLI

## Contributing

To add new tasks:

1. Add the task to the `AGENT_TASKS` list in `task_definitions.py`
2. Assign an appropriate agent in `TASK_AGENT_MAPPING`
3. Update dependencies if needed
4. Run `python task_cli.py list` to verify

## References

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [GitHub Issues](https://github.com/aicogniquest-glitch/agentic-platform/issues)
- Original requirements from GitHub issues #1-4
