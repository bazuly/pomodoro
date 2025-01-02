from database import get_db_connection
from cache.accessor import get_redis_connection
from fastapi import Depends
from repository import TaskRepository, TaskCache
from service.task import TaskService


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_connection()
    return TaskRepository(db_session)


def get_tasks_cache_repository() -> TaskCache:
    db_redis_session = get_redis_connection()
    return TaskCache(db_redis_session)


def get_task_service(
    task_repository: TaskRepository = Depends(get_tasks_repository),
    task_cache: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )
