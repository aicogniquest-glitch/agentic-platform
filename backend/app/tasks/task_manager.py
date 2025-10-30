"""
Task Manager for ADK Agent Tasks.

This module provides functionality to manage, load, and execute tasks
that have been converted from GitHub issues for ADK agents.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from .task_definitions import (
    AgentTask,
    TaskStatus,
    TaskComplexity,
    get_all_tasks,
    get_task_by_id,
    get_tasks_by_status,
    get_pending_tasks,
)
from ..agents.agent_definitions import (
    AgentDefinition,
    get_agent_for_task,
    get_all_agents,
)


class TaskManager:
    """
    Manages agent tasks including loading, status tracking, and execution coordination.
    """
    
    def __init__(self):
        """Initialize the task manager."""
        self.tasks = get_all_tasks()
        self.agents = get_all_agents()
    
    def get_all_tasks(self) -> List[AgentTask]:
        """Get all tasks."""
        return self.tasks
    
    def get_task(self, task_id: str) -> Optional[AgentTask]:
        """Get a specific task by ID."""
        return get_task_by_id(task_id)
    
    def get_pending_tasks(self) -> List[AgentTask]:
        """Get all pending tasks."""
        return get_pending_tasks()
    
    def get_tasks_by_complexity(self, complexity: TaskComplexity) -> List[AgentTask]:
        """Get tasks filtered by complexity."""
        return [task for task in self.tasks if task.complexity == complexity]
    
    def get_task_with_agent(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a task along with its recommended agent.
        
        Returns:
            Dictionary containing task and agent information, or None if task not found.
        """
        task = self.get_task(task_id)
        if not task:
            return None
        
        agent = get_agent_for_task(task_id)
        
        return {
            "task": task.to_dict(),
            "agent": agent.to_dict() if agent else None,
        }
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """
        Update the status of a task.
        
        Args:
            task_id: The task ID to update
            status: The new status
            
        Returns:
            True if update successful, False otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.status = status
            return True
        return False
    
    def export_tasks_to_json(self, filepath: str) -> None:
        """
        Export all tasks to a JSON file.
        
        Args:
            filepath: Path to the output JSON file
        """
        tasks_data = [task.to_dict() for task in self.tasks]
        
        with open(filepath, 'w') as f:
            json.dump(tasks_data, f, indent=2)
    
    def export_task_agent_mapping(self, filepath: str) -> None:
        """
        Export task-agent mapping to a JSON file.
        
        Args:
            filepath: Path to the output JSON file
        """
        mapping_data = []
        
        for task in self.tasks:
            agent = get_agent_for_task(task.task_id)
            mapping_data.append({
                "task_id": task.task_id,
                "task_title": task.title,
                "agent_name": agent.name if agent else None,
                "complexity": task.complexity.value,
                "estimated_hours": task.estimated_hours,
            })
        
        with open(filepath, 'w') as f:
            json.dump(mapping_data, f, indent=2)
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the tasks.
        
        Returns:
            Dictionary containing task statistics
        """
        total_tasks = len(self.tasks)
        pending = len([t for t in self.tasks if t.status == TaskStatus.PENDING])
        in_progress = len([t for t in self.tasks if t.status == TaskStatus.IN_PROGRESS])
        completed = len([t for t in self.tasks if t.status == TaskStatus.COMPLETED])
        failed = len([t for t in self.tasks if t.status == TaskStatus.FAILED])
        
        small_tasks = len([t for t in self.tasks if t.complexity == TaskComplexity.SMALL])
        medium_tasks = len([t for t in self.tasks if t.complexity == TaskComplexity.MEDIUM])
        large_tasks = len([t for t in self.tasks if t.complexity == TaskComplexity.LARGE])
        
        total_estimated_hours = sum(
            task.estimated_hours for task in self.tasks 
            if task.estimated_hours is not None
        )
        
        return {
            "total_tasks": total_tasks,
            "by_status": {
                "pending": pending,
                "in_progress": in_progress,
                "completed": completed,
                "failed": failed,
            },
            "by_complexity": {
                "small": small_tasks,
                "medium": medium_tasks,
                "large": large_tasks,
            },
            "total_estimated_hours": total_estimated_hours,
        }
    
    def get_dependency_order(self) -> List[str]:
        """
        Get tasks in dependency order (tasks with no dependencies first).
        
        Returns:
            List of task IDs in execution order
        """
        ordered_tasks = []
        remaining_tasks = {task.task_id: task for task in self.tasks}
        
        while remaining_tasks:
            # Find tasks with no unresolved dependencies
            ready_tasks = [
                task_id for task_id, task in remaining_tasks.items()
                if all(dep in ordered_tasks for dep in task.dependencies)
            ]
            
            if not ready_tasks:
                # If no tasks are ready, there might be a circular dependency
                # Add remaining tasks anyway
                ready_tasks = list(remaining_tasks.keys())
            
            for task_id in ready_tasks:
                ordered_tasks.append(task_id)
                del remaining_tasks[task_id]
        
        return ordered_tasks


# Global task manager instance
_task_manager = None


def get_task_manager() -> TaskManager:
    """Get or create the global task manager instance."""
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager()
    return _task_manager
