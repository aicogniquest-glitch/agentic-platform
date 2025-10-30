"""
Task definitions converted from GitHub issues for ADK agents.

Each task represents a GitHub issue converted into an ADK-compatible agent task format.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class TaskComplexity(str, Enum):
    """Task complexity levels."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    """
    Represents a task that can be executed by an ADK agent.
    
    This structure is designed to be compatible with Google's ADK framework,
    providing clear instructions, acceptance criteria, and metadata for agent execution.
    """
    task_id: str
    title: str
    description: str
    instruction: str  # Clear operational goal for the agent
    acceptance_criteria: List[str]
    complexity: TaskComplexity
    labels: List[str]
    tools_required: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    github_issue_number: Optional[int] = None
    estimated_hours: Optional[float] = None
    subtasks: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary format for serialization."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "instruction": self.instruction,
            "acceptance_criteria": self.acceptance_criteria,
            "complexity": self.complexity.value,
            "labels": self.labels,
            "tools_required": self.tools_required,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "github_issue_number": self.github_issue_number,
            "estimated_hours": self.estimated_hours,
            "subtasks": self.subtasks,
        }
    
    @classmethod
    def from_github_issue(cls, issue_number: int, title: str, body: str, 
                         labels: List[str]) -> "AgentTask":
        """
        Create an AgentTask from a GitHub issue.
        
        Args:
            issue_number: GitHub issue number
            title: Issue title
            body: Issue body/description
            labels: Issue labels
            
        Returns:
            AgentTask instance
        """
        # Parse acceptance criteria from body
        acceptance_criteria = []
        description = body
        complexity = TaskComplexity.MEDIUM
        
        if "**Acceptance Criteria:**" in body:
            parts = body.split("**Acceptance Criteria:**")
            description = parts[0].strip()
            criteria_section = parts[1].split("**Complexity:**")[0] if "**Complexity:**" in parts[1] else parts[1]
            acceptance_criteria = [
                line.strip("- ").strip() 
                for line in criteria_section.split("\n") 
                if line.strip().startswith("-")
            ]
        
        # Parse complexity
        if "**Complexity:**" in body:
            complexity_text = body.split("**Complexity:**")[1].split("\n")[0].strip().lower()
            if complexity_text in ["small", "medium", "large"]:
                complexity = TaskComplexity(complexity_text)
        
        # Generate task ID from issue number
        task_id = f"task_{issue_number:04d}"
        
        # Create instruction for agent
        instruction = f"Complete the task: {title}. {description}"
        
        return cls(
            task_id=task_id,
            title=title,
            description=description,
            instruction=instruction,
            acceptance_criteria=acceptance_criteria,
            complexity=complexity,
            labels=labels,
            github_issue_number=issue_number,
        )


# Task definitions converted from GitHub issues
AGENT_TASKS: List[AgentTask] = [
    AgentTask(
        task_id="task_0001",
        title="Develop execution panel and monitoring dashboard",
        description=(
            "Build React components for live execution monitoring, agent/workflow analytics, "
            "and results viewing in frontend/src/components/Execution and "
            "frontend/src/components/Dashboard. These components should visualize execution "
            "progress, logs, and performance metrics."
        ),
        instruction=(
            "Create a comprehensive execution monitoring and dashboard system for the agentic platform. "
            "Focus on building React components that provide real-time visibility into agent and workflow "
            "executions, including progress tracking, logs, and performance analytics. Ensure the UI is "
            "intuitive and provides actionable insights for users."
        ),
        acceptance_criteria=[
            "Execution panel component in frontend/src/components/Execution created",
            "Dashboard component in frontend/src/components/Dashboard created",
            "Live execution monitoring with real-time updates implemented",
            "Agent and workflow analytics visualization completed",
            "Results viewing interface with detailed logs functional",
            "Performance metrics display integrated",
        ],
        complexity=TaskComplexity.LARGE,
        labels=["enhancement", "frontend", "dashboard"],
        tools_required=["react", "material-ui", "websocket", "charting-library"],
        dependencies=[],
        github_issue_number=1,
        estimated_hours=40.0,
        subtasks=[
            "Create Execution panel component structure",
            "Implement real-time WebSocket connection for live updates",
            "Build Dashboard layout with analytics widgets",
            "Create log viewer component with filtering",
            "Implement performance metrics charts",
            "Add execution history and state management",
        ],
    ),
    AgentTask(
        task_id="task_0002",
        title="Create ADK configuration module",
        description=(
            "Implement the configuration module in backend/app/config.py to manage all "
            "environment variables and ADK settings for the platform."
        ),
        instruction=(
            "Develop a robust configuration management system for the agentic platform that handles "
            "all environment variables, ADK settings, and application configuration. The module should "
            "provide type-safe access to configuration values, support multiple environments, and "
            "integrate seamlessly with the ADK framework."
        ),
        acceptance_criteria=[
            "Configuration module in backend/app/config.py created",
            "Environment variable management implemented",
            "ADK-specific settings configured",
            "Type-safe configuration access provided",
            "Support for multiple environments (dev, prod, test)",
            "Configuration validation and defaults implemented",
        ],
        complexity=TaskComplexity.MEDIUM,
        labels=["enhancement", "backend", "configuration"],
        tools_required=["python", "pydantic-settings", "python-dotenv"],
        dependencies=[],
        github_issue_number=2,
        estimated_hours=8.0,
        subtasks=[
            "Create base configuration class using Pydantic",
            "Define ADK-specific settings (model, API keys)",
            "Implement environment variable loading",
            "Add configuration validation",
            "Create configuration factory for different environments",
            "Add unit tests for configuration module",
        ],
    ),
    AgentTask(
        task_id="task_0003",
        title="Implement React frontend with Agent, Tool, and Workflow Builders",
        description=(
            "Set up the React frontend in frontend/src/components/ with AgentBuilder, ToolBuilder, "
            "and WorkflowBuilder components. These should provide a visual interface for users to "
            "create agents, tools, and workflows leveraging ADK functionalities."
        ),
        instruction=(
            "Build a comprehensive visual builder interface for the agentic platform that allows users "
            "to create and configure agents, tools, and workflows without writing code. The interface "
            "should use drag-and-drop functionality, node-based editing, and provide real-time validation. "
            "Integrate with the ADK framework to ensure created components are compatible."
        ),
        acceptance_criteria=[
            "AgentBuilder, ToolBuilder, WorkflowBuilder components implemented",
            "User can create and configure agents, tools, workflows visually",
            "UI uses Material-UI and ReactFlow for node-based editing",
            "Frontend communicates with backend API",
            "Real-time validation of configurations",
            "Export/import functionality for agents, tools, and workflows",
        ],
        complexity=TaskComplexity.LARGE,
        labels=["frontend", "adk", "high-priority", "enhancement"],
        tools_required=["react", "material-ui", "reactflow", "form-validation"],
        dependencies=["task_0002"],  # Depends on config module
        github_issue_number=3,
        estimated_hours=60.0,
        subtasks=[
            "Set up React project structure in frontend/",
            "Implement AgentBuilder component with form inputs",
            "Create ToolBuilder with visual configuration",
            "Build WorkflowBuilder using ReactFlow for node-based editing",
            "Implement drag-and-drop functionality",
            "Add validation and error handling",
            "Create API integration layer",
            "Implement save/load functionality",
            "Add export/import for configurations",
        ],
    ),
    AgentTask(
        task_id="task_0004",
        title="Build backend service layer for business logic",
        description=(
            "Create backend service modules in backend/app/services/ to handle business logic "
            "for agents, tools, workflows, and executions. Service layer should interact with "
            "ADK modules and database models."
        ),
        instruction=(
            "Develop a clean service layer architecture for the agentic platform that separates "
            "business logic from API endpoints. Create service classes for managing agents, tools, "
            "workflows, and executions. Ensure proper integration with the ADK framework and database "
            "models, following SOLID principles and best practices for maintainable code."
        ),
        acceptance_criteria=[
            "Service classes for agent, tool, workflow, execution",
            "Separation of concerns between API and business logic",
            "Unit tests for service layer",
            "Integration with ADK modules",
            "Database model interactions implemented",
            "Error handling and validation in place",
        ],
        complexity=TaskComplexity.MEDIUM,
        labels=["backend", "enhancement"],
        tools_required=["python", "fastapi", "sqlalchemy", "google-adk"],
        dependencies=["task_0002"],  # Depends on config module
        github_issue_number=4,
        estimated_hours=24.0,
        subtasks=[
            "Create service layer directory structure",
            "Implement AgentService class",
            "Implement ToolService class",
            "Implement WorkflowService class",
            "Implement ExecutionService class",
            "Add database model interactions",
            "Implement error handling and validation",
            "Create unit tests for each service",
            "Add integration tests with ADK",
        ],
    ),
]


def get_all_tasks() -> List[AgentTask]:
    """Get all defined agent tasks."""
    return AGENT_TASKS


def get_task_by_id(task_id: str) -> Optional[AgentTask]:
    """Get a task by its ID."""
    for task in AGENT_TASKS:
        if task.task_id == task_id:
            return task
    return None


def get_tasks_by_status(status: TaskStatus) -> List[AgentTask]:
    """Get all tasks with a specific status."""
    return [task for task in AGENT_TASKS if task.status == status]


def get_tasks_by_complexity(complexity: TaskComplexity) -> List[AgentTask]:
    """Get all tasks with a specific complexity level."""
    return [task for task in AGENT_TASKS if task.complexity == complexity]


def get_pending_tasks() -> List[AgentTask]:
    """Get all pending tasks."""
    return get_tasks_by_status(TaskStatus.PENDING)
