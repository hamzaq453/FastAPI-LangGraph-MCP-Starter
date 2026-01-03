"""Database models using SQLModel.

SQLModel combines SQLAlchemy and Pydantic for type-safe database models.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    """TODO item model for database storage."""
    
    __tablename__ = "todos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str = Field(max_length=500, nullable=False)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "task": "Buy groceries",
                "completed": False,
            }
        }
