"""Database models for the application."""
from datetime import datetime
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Task(db.Model):
    """Task model."""
    
    __tablename__ = "tasks"
    
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(200), nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)
    completed: bool = db.Column(db.Boolean, default=False)
    created_at: datetime = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: datetime = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }