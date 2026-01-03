"""Simple in-memory TODO management for agent tools.

This provides synchronous TODO operations for the LangGraph agent.
For persistent database-backed TODOs, use app.mcp.tools.todo module directly.
"""

from typing import Any

# In-memory storage
_todos: dict[int, dict[str, Any]] = {}
_next_id = 1


def add_todo(task: str) -> dict[str, Any]:
    """
    Add a new TODO item.
    
    Args:
        task: Description of the task
        
    Returns:
        Created TODO with id, task, and completed status
    """
    global _next_id
    
    todo = {
        "id": _next_id,
        "task": task,
        "completed": False,
    }
    _todos[_next_id] = todo
    _next_id += 1
    
    return todo


def list_todos() -> list[dict[str, Any]]:
    """
    Get all TODO items.
    
    Returns:
        List of all TODOs
    """
    return list(_todos.values())


def complete_todo(todo_id: int) -> dict[str, Any]:
    """
    Mark a TODO as completed.
    
    Args:
        todo_id: ID of the TODO to complete
        
    Returns:
        Updated TODO
        
    Raises:
        ValueError: If TODO not found
    """
    if todo_id not in _todos:
        raise ValueError(f"TODO {todo_id} not found")
    
    _todos[todo_id]["completed"] = True
    return _todos[todo_id]


def delete_todo(todo_id: int) -> dict[str, str]:
    """
    Delete a TODO item.
    
    Args:
        todo_id: ID of the TODO to delete
        
    Returns:
        Success message
        
    Raises:
        ValueError: If TODO not found
    """
    if todo_id not in _todos:
        raise ValueError(f"TODO {todo_id} not found")
    
    del _todos[todo_id]
    return {"message": f"TODO {todo_id} deleted"}


def clear_todos() -> dict[str, str]:
    """
    Clear all TODOs.
    
    Returns:
        Success message
    """
    _todos.clear()
    return {"message": "All TODOs cleared"}
