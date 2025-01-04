from database import get_db_connection
from cache.accessor import get_redis_connection
from fastapi import Depends
from repository import TaskRepository, TaskCache, UserRepository
from service.task import TaskService
from service.user import UserService
from service.auth import AuthService
from sqlalchemy.orm import Session


def get_tasks_repository(db_session: Session = Depends(get_db_connection)) -> TaskRepository:
    return TaskRepository(db_session=db_session)


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


def get_user_repository(db_session: Session = Depends(get_db_connection)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(
        user_repository=user_repository
    )


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(
        user_repository=user_repository
    )
