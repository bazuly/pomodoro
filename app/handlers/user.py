from typing import Annotated

from fastapi import APIRouter, Depends

from app.schema.user import UserCreateSchema, UserLoginSchema
from app.service.user import UserService
from app.dependency import get_user_service

router = APIRouter(prefix="/user", tags=['user'])


@router.post(
    "/create_user",
    response_model=UserLoginSchema
)
async def create_user(
        body: UserCreateSchema,
        user_repository: Annotated[UserService, Depends(get_user_service)]
):
    return await user_repository.create_user(
        username=body.username,
        password=body.password
    )
