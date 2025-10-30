"""
Example integration of tasks with Google ADK agents.

This module demonstrates how to use the task definitions with ADK agents
for automated execution.
"""

# Note: This is example code showing how tasks integrate with ADK
# Actual ADK usage would require the google-adk package installed

from typing import Dict, Any, Optional


class MockADKAgent:
    """
    Mock ADK Agent class for demonstration purposes.
    
    In a real implementation, this would be replaced with:
    from adk import Agent
    """
    
    def __init__(self, name: str, model: str, instruction: str, tools: list):
        self.name = name
        self.model = model
        self.instruction = instruction
        self.tools = tools
        print(f"Initialized {name} with model {model}")
    
    def execute(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task (mock implementation).
        
        Args:
            task_context: Context information for task execution
            
        Returns:
            Result dictionary
        """
        print(f"\n{self.name} is executing task:")
        print(f"Instruction: {self.instruction}")
        print(f"Tools available: {', '.join(self.tools)}")
        
        return {
            "status": "success",
            "message": f"Task executed by {self.name}",
            "agent": self.name,
        }


def create_agent_from_definition(agent_def: Dict[str, Any]) -> MockADKAgent:
    """
    Create an ADK agent from an agent definition.
    
    Args:
        agent_def: Agent definition dictionary
        
    Returns:
        ADK Agent instance
    """
    return MockADKAgent(
        name=agent_def["name"],
        model=agent_def["model"],
        instruction=agent_def["instruction"],
        tools=agent_def["tools"],
    )


def execute_task_with_agent(task_id: str) -> Optional[Dict[str, Any]]:
    """
    Execute a task using its assigned ADK agent.
    
    Args:
        task_id: The task ID to execute
        
    Returns:
        Execution result or None if task not found
    """
    from app.tasks.task_manager import get_task_manager
    from app.tasks.task_definitions import TaskStatus
    
    manager = get_task_manager()
    
    # Get task with agent
    task_info = manager.get_task_with_agent(task_id)
    
    if not task_info:
        print(f"Task {task_id} not found")
        return None
    
    task = task_info["task"]
    agent_def = task_info["agent"]
    
    if not agent_def:
        print(f"No agent assigned to task {task_id}")
        return None
    
    print(f"\n{'=' * 80}")
    print(f"EXECUTING TASK: {task['task_id']}")
    print(f"Title: {task['title']}")
    print(f"{'=' * 80}")
    
    # Create agent
    agent = create_agent_from_definition(agent_def)
    
    # Prepare task context
    task_context = {
        "task_id": task["task_id"],
        "title": task["title"],
        "description": task["description"],
        "acceptance_criteria": task["acceptance_criteria"],
        "subtasks": task["subtasks"],
        "tools_required": task["tools_required"],
    }
    
    # Mark task as in progress
    manager.update_task_status(task_id, TaskStatus.IN_PROGRESS)
    
    # Execute task
    result = agent.execute(task_context)
    
    # Update task status based on result
    if result.get("status") == "success":
        manager.update_task_status(task_id, TaskStatus.COMPLETED)
        print(f"\n✓ Task {task_id} completed successfully!")
    else:
        manager.update_task_status(task_id, TaskStatus.FAILED)
        print(f"\n✗ Task {task_id} failed!")
    
    return result


def execute_all_pending_tasks():
    """Execute all pending tasks in dependency order."""
    from app.tasks.task_manager import get_task_manager
    
    manager = get_task_manager()
    
    # Get tasks in dependency order
    task_order = manager.get_dependency_order()
    
    print("\n" + "=" * 80)
    print("EXECUTING ALL PENDING TASKS")
    print("=" * 80)
    
    results = []
    
    for task_id in task_order:
        task = manager.get_task(task_id)
        
        # Check if dependencies are completed
        from app.tasks.task_definitions import TaskStatus as TS
        dependencies_met = all(
            manager.get_task(dep_id).status == TS.COMPLETED
            for dep_id in task.dependencies
        )
        
        if not dependencies_met:
            print(f"\n⚠ Skipping {task_id} - dependencies not met")
            continue
        
        result = execute_task_with_agent(task_id)
        results.append({
            "task_id": task_id,
            "result": result,
        })
    
    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    
    stats = manager.get_task_statistics()
    print(f"\nCompleted: {stats['by_status']['completed']}")
    print(f"Failed: {stats['by_status']['failed']}")
    print(f"Pending: {stats['by_status']['pending']}")
    print(f"In Progress: {stats['by_status']['in_progress']}")
    
    return results


def main():
    """Main entry point for example execution."""
    import sys
    
    if len(sys.argv) > 1:
        # Execute specific task
        task_id = sys.argv[1]
        execute_task_with_agent(task_id)
    else:
        # Execute all pending tasks
        execute_all_pending_tasks()


if __name__ == "__main__":
    main()
