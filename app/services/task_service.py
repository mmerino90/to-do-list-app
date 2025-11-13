"""Task service module."""
from typing import List, Optional
from datetime import datetime, timedelta
from app.extensions import db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.constants import DUPLICATE_CHECK_WINDOW_SECONDS


class TaskService:
    """Service for handling task operations.
    
    Implements single responsibility principle:
    - Handles all business logic for task management
    - Abstracts database operations
    - No HTTP concerns (status codes, responses, etc.)
    """

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
        # Use Session.get() instead of Query.get() (SQLAlchemy 2.x)
        return db.session.get(Task, task_id)

    @staticmethod
    def create_task(task_data: TaskCreate) -> Task:
        """Create a new task with deduplication check.
        
        Prevents duplicate tasks from being created if an identical
        task (same title and description) was created within the
        deduplication window.
        
        Args:
            task_data: Task creation data
            
        Returns:
            Created or existing task
        """
        # Check for duplicates within the deduplication window
        recent_duplicate = TaskService._find_recent_duplicate(task_data)
        if recent_duplicate:
            return recent_duplicate

        task = Task(title=task_data.title, description=task_data.description)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def _find_recent_duplicate(task_data: TaskCreate) -> Optional[Task]:
        """Find a recently created task matching the given data.
        
        Args:
            task_data: Task data to match
            
        Returns:
            Matching task if found within deduplication window, None otherwise
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=DUPLICATE_CHECK_WINDOW_SECONDS)
        recent = (
            Task.query.filter(
                Task.title == task_data.title,
                Task.description == task_data.description,
                Task.created_at >= window_start,
            )
            .order_by(Task.created_at.desc())
            .first()
        )  # type: ignore[attr-defined]
        return recent

    @staticmethod
    def update_task(task: Task, task_data: TaskUpdate) -> Task:
        """Update an existing task."""
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task: Task) -> None:
        """Delete a task."""
        db.session.delete(task)
        db.session.commit()
