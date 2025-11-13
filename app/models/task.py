"""Database models for the application."""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.sql import func
from app.extensions import db


class Task(db.Model):  # type: ignore[name-defined]
    """Task model representing a to-do item.
    
    Attributes:
        id: Unique identifier
        title: Task title (required, max 200 chars)
        description: Optional task description
        completed: Whether task is completed (default False)
        created_at: Creation timestamp (server-generated)
        updated_at: Last update timestamp (server-generated)
    """

    __tablename__ = "tasks"

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(200), nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)
    completed: bool = db.Column(db.Boolean, default=False)
    created_at: datetime = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )
    updated_at: datetime = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the task with ISO-formatted timestamps
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation of the task."""
        return f"<Task {self.id}: {self.title}>"
