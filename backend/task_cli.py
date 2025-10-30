#!/usr/bin/env python3
"""
CLI tool for managing ADK agent tasks.

This tool allows you to view, export, and manage tasks that have been
converted from GitHub issues for execution by ADK agents.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.tasks.task_manager import get_task_manager
from app.tasks.task_definitions import TaskStatus, TaskComplexity


def list_tasks(args):
    """List all tasks or filter by status/complexity."""
    manager = get_task_manager()
    
    tasks = manager.get_all_tasks()
    
    # Apply filters
    if args.status:
        status = TaskStatus(args.status)
        tasks = [t for t in tasks if t.status == status]
    
    if args.complexity:
        complexity = TaskComplexity(args.complexity)
        tasks = [t for t in tasks if t.complexity == complexity]
    
    if not tasks:
        print("No tasks found matching the criteria.")
        return
    
    print(f"\nFound {len(tasks)} task(s):\n")
    
    for task in tasks:
        print(f"Task ID: {task.task_id}")
        print(f"Title: {task.title}")
        print(f"Status: {task.status.value}")
        print(f"Complexity: {task.complexity.value}")
        if task.estimated_hours:
            print(f"Estimated Hours: {task.estimated_hours}")
        if task.github_issue_number:
            print(f"GitHub Issue: #{task.github_issue_number}")
        print(f"Labels: {', '.join(task.labels)}")
        print("-" * 80)


def show_task(args):
    """Show detailed information about a specific task."""
    manager = get_task_manager()
    
    task_data = manager.get_task_with_agent(args.task_id)
    
    if not task_data:
        print(f"Task {args.task_id} not found.")
        return
    
    task = task_data["task"]
    agent = task_data["agent"]
    
    print(f"\n{'=' * 80}")
    print(f"TASK: {task['task_id']}")
    print(f"{'=' * 80}\n")
    
    print(f"Title: {task['title']}")
    print(f"Status: {task['status']}")
    print(f"Complexity: {task['complexity']}")
    if task.get('estimated_hours'):
        print(f"Estimated Hours: {task['estimated_hours']}")
    if task.get('github_issue_number'):
        print(f"GitHub Issue: #{task['github_issue_number']}")
    
    print(f"\nDescription:")
    print(f"{task['description']}\n")
    
    print(f"Instruction for Agent:")
    print(f"{task['instruction']}\n")
    
    if task['acceptance_criteria']:
        print("Acceptance Criteria:")
        for i, criterion in enumerate(task['acceptance_criteria'], 1):
            print(f"  {i}. {criterion}")
        print()
    
    if task['subtasks']:
        print("Subtasks:")
        for i, subtask in enumerate(task['subtasks'], 1):
            print(f"  {i}. {subtask}")
        print()
    
    if task['dependencies']:
        print(f"Dependencies: {', '.join(task['dependencies'])}\n")
    
    if task['tools_required']:
        print(f"Tools Required: {', '.join(task['tools_required'])}\n")
    
    print(f"Labels: {', '.join(task['labels'])}\n")
    
    if agent:
        print(f"{'=' * 80}")
        print(f"RECOMMENDED AGENT: {agent['name']}")
        print(f"{'=' * 80}\n")
        print(f"Model: {agent['model']}")
        print(f"Description: {agent['description']}\n")
        print(f"Capabilities:")
        for capability in agent['capabilities']:
            print(f"  - {capability}")
        print()


def export_tasks(args):
    """Export tasks to a JSON file."""
    manager = get_task_manager()
    
    output_path = args.output or "tasks.json"
    manager.export_tasks_to_json(output_path)
    
    print(f"Tasks exported to {output_path}")


def export_mapping(args):
    """Export task-agent mapping to a JSON file."""
    manager = get_task_manager()
    
    output_path = args.output or "task_agent_mapping.json"
    manager.export_task_agent_mapping(output_path)
    
    print(f"Task-agent mapping exported to {output_path}")


def show_statistics(args):
    """Show statistics about tasks."""
    manager = get_task_manager()
    
    stats = manager.get_task_statistics()
    
    print(f"\n{'=' * 80}")
    print("TASK STATISTICS")
    print(f"{'=' * 80}\n")
    
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"Total Estimated Hours: {stats['total_estimated_hours']:.1f}\n")
    
    print("By Status:")
    for status, count in stats['by_status'].items():
        print(f"  {status.capitalize()}: {count}")
    print()
    
    print("By Complexity:")
    for complexity, count in stats['by_complexity'].items():
        print(f"  {complexity.capitalize()}: {count}")
    print()


def show_dependency_order(args):
    """Show tasks in dependency order."""
    manager = get_task_manager()
    
    ordered_task_ids = manager.get_dependency_order()
    
    print("\nTasks in dependency order (execute in this order):\n")
    
    for i, task_id in enumerate(ordered_task_ids, 1):
        task = manager.get_task(task_id)
        dependencies_str = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
        print(f"{i}. {task_id}: {task.title}{dependencies_str}")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Manage ADK agent tasks converted from GitHub issues"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "completed", "failed"],
        help="Filter by status"
    )
    list_parser.add_argument(
        "--complexity",
        choices=["small", "medium", "large"],
        help="Filter by complexity"
    )
    list_parser.set_defaults(func=list_tasks)
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show detailed task information")
    show_parser.add_argument("task_id", help="Task ID to show")
    show_parser.set_defaults(func=show_task)
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export tasks to JSON")
    export_parser.add_argument(
        "--output", "-o",
        help="Output file path (default: tasks.json)"
    )
    export_parser.set_defaults(func=export_tasks)
    
    # Export mapping command
    mapping_parser = subparsers.add_parser(
        "export-mapping",
        help="Export task-agent mapping to JSON"
    )
    mapping_parser.add_argument(
        "--output", "-o",
        help="Output file path (default: task_agent_mapping.json)"
    )
    mapping_parser.set_defaults(func=export_mapping)
    
    # Statistics command
    stats_parser = subparsers.add_parser("stats", help="Show task statistics")
    stats_parser.set_defaults(func=show_statistics)
    
    # Dependency order command
    deps_parser = subparsers.add_parser(
        "dependency-order",
        help="Show tasks in dependency order"
    )
    deps_parser.set_defaults(func=show_dependency_order)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
