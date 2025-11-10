"""Task schemas for request/response validation."""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base task schema."""
    
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    """Schema for task creation."""
    pass


class TaskUpdate(BaseModel):
    """Schema for task update."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskInDB(TaskBase):
    """Schema for task in database."""
    
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True