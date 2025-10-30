"""
ADK Agent definitions for executing platform tasks.

This module defines agents that can execute the converted GitHub issue tasks
using Google's Agent Development Kit (ADK).
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AgentDefinition:
    """
    Represents an ADK agent configuration for executing tasks.
    
    This structure follows the Google ADK agent definition format with:
    - name: Unique identifier for the agent
    - model: The LLM model to use (e.g., gemini-2.5-pro, gpt-4)
    - instruction: The agent's operational goal
    - tools: List of tools/functions the agent can use
    - callbacks: Functions for monitoring and control
    """
    name: str
    model: str
    instruction: str
    description: str
    tools: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    task_types: List[str] = field(default_factory=list)
    before_agent_callback: Optional[str] = None
    after_agent_callback: Optional[str] = None
    after_tool_callback: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent definition to dictionary for serialization."""
        return {
            "name": self.name,
            "model": self.model,
            "instruction": self.instruction,
            "description": self.description,
            "tools": self.tools,
            "capabilities": self.capabilities,
            "task_types": self.task_types,
            "before_agent_callback": self.before_agent_callback,
            "after_agent_callback": self.after_agent_callback,
            "after_tool_callback": self.after_tool_callback,
        }


# Agent definitions for different task types
AGENT_DEFINITIONS: List[AgentDefinition] = [
    AgentDefinition(
        name="FrontendDeveloperAgent",
        model="gemini-2.5-pro",
        instruction=(
            "You are an expert frontend developer specializing in React, Material-UI, and modern "
            "JavaScript frameworks. Your role is to build user interfaces, implement React components, "
            "and ensure responsive, accessible, and performant web applications. You excel at creating "
            "visual builders, dashboards, and interactive UI components."
        ),
        description=(
            "Frontend development agent responsible for React component development, UI/UX implementation, "
            "and client-side application logic."
        ),
        tools=[
            "code_editor",
            "file_system",
            "npm_package_manager",
            "browser_dev_tools",
            "git_operations",
        ],
        capabilities=[
            "React component development",
            "Material-UI implementation",
            "ReactFlow node-based editing",
            "WebSocket integration",
            "Frontend testing with Jest/React Testing Library",
            "State management (Redux, Context API)",
            "API integration",
            "Responsive design",
        ],
        task_types=["frontend", "ui", "dashboard", "visualization"],
        after_tool_callback="validate_frontend_output",
    ),
    AgentDefinition(
        name="BackendDeveloperAgent",
        model="gemini-2.5-pro",
        instruction=(
            "You are an expert backend developer proficient in Python, FastAPI, SQLAlchemy, and "
            "database design. Your role is to build robust service layers, implement business logic, "
            "create RESTful APIs, and ensure secure, scalable backend systems. You excel at integrating "
            "with frameworks like Google ADK and managing data persistence."
        ),
        description=(
            "Backend development agent responsible for service layer implementation, API development, "
            "database management, and ADK integration."
        ),
        tools=[
            "code_editor",
            "file_system",
            "pip_package_manager",
            "database_client",
            "api_testing_tool",
            "git_operations",
        ],
        capabilities=[
            "FastAPI development",
            "SQLAlchemy ORM",
            "Service layer architecture",
            "RESTful API design",
            "Database schema design",
            "Google ADK integration",
            "Authentication and authorization",
            "Backend testing with pytest",
        ],
        task_types=["backend", "api", "service", "database"],
        after_tool_callback="validate_backend_output",
    ),
    AgentDefinition(
        name="ConfigurationAgent",
        model="gemini-2.5-pro",
        instruction=(
            "You are an expert in application configuration management and environment setup. "
            "Your role is to create robust configuration modules, manage environment variables, "
            "implement settings validation, and ensure proper configuration for different deployment "
            "environments. You excel at using Pydantic for type-safe configuration and python-dotenv "
            "for environment management."
        ),
        description=(
            "Configuration management agent responsible for setting up environment variables, "
            "application settings, and ADK configuration."
        ),
        tools=[
            "code_editor",
            "file_system",
            "environment_manager",
            "validation_tools",
            "git_operations",
        ],
        capabilities=[
            "Pydantic Settings implementation",
            "Environment variable management",
            "Configuration validation",
            "Multi-environment support",
            "Secrets management",
            "Type-safe configuration",
        ],
        task_types=["configuration", "setup", "environment"],
        after_tool_callback="validate_configuration",
    ),
    AgentDefinition(
        name="FullStackAgent",
        model="gemini-2.5-pro",
        instruction=(
            "You are a versatile full-stack developer capable of working on both frontend and backend "
            "components. Your role is to implement end-to-end features, ensure frontend-backend integration, "
            "and deliver complete functionalities. You have expertise in React, FastAPI, databases, and "
            "modern development practices."
        ),
        description=(
            "Full-stack development agent capable of handling both frontend and backend tasks, "
            "including integration work."
        ),
        tools=[
            "code_editor",
            "file_system",
            "npm_package_manager",
            "pip_package_manager",
            "database_client",
            "api_testing_tool",
            "browser_dev_tools",
            "git_operations",
        ],
        capabilities=[
            "Full-stack development",
            "Frontend-backend integration",
            "API design and implementation",
            "React development",
            "FastAPI development",
            "Database operations",
            "End-to-end testing",
        ],
        task_types=["fullstack", "integration", "feature", "enhancement"],
        after_tool_callback="validate_integration",
    ),
]


# Task-to-Agent mapping
TASK_AGENT_MAPPING = {
    "task_0001": "FrontendDeveloperAgent",  # Execution panel and dashboard
    "task_0002": "ConfigurationAgent",       # ADK configuration module
    "task_0003": "FrontendDeveloperAgent",  # React builders
    "task_0004": "BackendDeveloperAgent",   # Backend service layer
}


def get_all_agents() -> List[AgentDefinition]:
    """Get all defined agents."""
    return AGENT_DEFINITIONS


def get_agent_by_name(name: str) -> Optional[AgentDefinition]:
    """Get an agent by name."""
    for agent in AGENT_DEFINITIONS:
        if agent.name == name:
            return agent
    return None


def get_agent_for_task(task_id: str) -> Optional[AgentDefinition]:
    """Get the recommended agent for a specific task."""
    agent_name = TASK_AGENT_MAPPING.get(task_id)
    if agent_name:
        return get_agent_by_name(agent_name)
    return None


def get_agents_by_capability(capability: str) -> List[AgentDefinition]:
    """Get all agents that have a specific capability."""
    return [
        agent for agent in AGENT_DEFINITIONS 
        if capability.lower() in [c.lower() for c in agent.capabilities]
    ]


def get_agents_by_task_type(task_type: str) -> List[AgentDefinition]:
    """Get all agents that can handle a specific task type."""
    return [
        agent for agent in AGENT_DEFINITIONS 
        if task_type.lower() in [t.lower() for t in agent.task_types]
    ]
