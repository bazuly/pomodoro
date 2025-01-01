from repository import TaskRepository
from database import get_db_connection


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_connection()
    return TaskRepository(db_session)
