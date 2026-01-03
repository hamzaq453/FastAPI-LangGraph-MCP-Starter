"""TODO management tool with PostgreSQL backend.

Provides CRUD operations for TODO items with database persistence.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Todo


async def add_todo(task: str, session: AsyncSession) -> dict[str, Any]:
    """
    Add a new TODO item to the database.
    
    Args:
        task: Description of the task to add
        session: Database session
        
    Returns:
        Created TODO item with id, task, and completed status
    """
    todo = Todo(task=task)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    
    return {
        "id": todo.id,
        "task": todo.task,
        "completed": todo.completed,
    }


async def list_todos(session: AsyncSession) -> list[dict[str, Any]]:
    """
    Get all TODO items from the database.
    
    Args:
        session: Database session
        
    Returns:
        List of all TODO items
    """
    result = await session.execute(select(Todo))
    todos = result.scalars().all()
    
    return [
        {
            "id": todo.id,
            "task": todo.task,
            "completed": todo.completed,
        }
        for todo in todos
    ]


async def complete_todo(todo_id: int, session: AsyncSession) -> dict[str, Any]:
    """
    Mark a TODO item as completed.
    
    Args:
        todo_id: ID of the TODO to mark as complete
        session: Database session
        
    Returns:
        Updated TODO item
        
    Raises:
        ValueError: If TODO with given ID doesn't exist
    """
    result = await session.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    
    if not todo:
        raise ValueError(f"TODO with id {todo_id} not found")
    
    todo.completed = True
    todo.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(todo)
    
    return {
        "id": todo.id,
        "task": todo.task,
        "completed": todo.completed,
    }


async def delete_todo(todo_id: int, session: AsyncSession) -> dict[str, str]:
    """
    Delete a TODO item from the database.
    
    Args:
        todo_id: ID of the TODO to delete
        session: Database session
        
    Returns:
        Success message
        
    Raises:
        ValueError: If TODO with given ID doesn't exist
    """
    result = await session.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    
    if not todo:
        raise ValueError(f"TODO with id {todo_id} not found")
    
    await session.delete(todo)
    await session.commit()
    
    return {"message": f"TODO {todo_id} deleted successfully"}


async def clear_todos(session: AsyncSession) -> dict[str, str]:
    """
    Clear all TODO items (useful for testing).
    
    Args:
        session: Database session
        
    Returns:
        Success message
    """
    await session.execute(update(Todo))
    result = await session.execute(select(Todo))
    todos = result.scalars().all()
    
    for todo in todos:
        await session.delete(todo)
    
    await session.commit()
    
    return {"message": "All TODOs cleared"}
