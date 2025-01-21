import httpx
from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.auth.client import GoogleClient, YandexClient
from app.infrastructure.database import get_db_connection
from app.infrastructure.cache.accessor import get_redis_connection

from .exception import TokenExpired, TokenNotCorrect
from .tasks.repository import TaskRepository, TaskCache
from .tasks.service import TaskService
from .users.auth.service import AuthService
from .users.user_profile.repository import UserRepository
from .users.user_profile.service import UserService
from settings import Settings


async def get_tasks_repository(db_session: AsyncSession = Depends(get_db_connection)) -> TaskRepository:
    return TaskRepository(db_session=db_session)


async def get_tasks_cache_repository() -> TaskCache:
    db_redis_session = get_redis_connection()
    return TaskCache(db_redis_session)


async def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_user_repository(db_session: AsyncSession = Depends(get_db_connection)) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    client = httpx.AsyncClient()
    try:
        yield client
    finally:
        await client.aclose()


async def get_google_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


async def get_yandex_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)

) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client

    )


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(
            reusable_oauth2)
) -> int | None:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    return user_id
