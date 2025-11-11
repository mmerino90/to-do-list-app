"""Task service module."""
from typing import List, Optional
from datetime import datetime, timedelta
from app.extensions import db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Service for handling task operations."""
    
    @staticmethod
    def get_all_tasks() -> List[Task]:
        """Get all tasks."""
        query = Task.query.order_by(
            Task.created_at.desc()  # type: ignore[attr-defined]
        )
        return query.all()  # type: ignore[attr-defined]
    
    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return Task.query.get(task_id)
    
    @staticmethod
    def create_task(task_data: TaskCreate) -> Task:
        """Create a new task."""
        # Simple deduplication: if an identical task (title+description) was created
        # in the last 2 seconds, return it instead of creating a duplicate. This
        # guards against accidental duplicate requests from clients.
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=2)
        recent = Task.query.filter(
            Task.title == task_data.title,
            Task.description == task_data.description,
            Task.created_at >= window_start
        ).order_by(Task.created_at.desc()).first()  # type: ignore[attr-defined]
        if recent:
            return recent

        task = Task(
            title=task_data.title,
            description=task_data.description
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def update_task(task: Task, task_data: TaskUpdate) -> Task:
        """Update an existing task."""
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        db.session.commit()
        return task
    
    @staticmethod
    def delete_task(task: Task) -> None:
        """Delete a task."""
        db.session.delete(task)
        db.session.commit()