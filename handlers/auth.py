from dependency import get_auth_service
from exception import UserNotFoundException, UserNotCorrectPasswordException
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from schema.user import UserCreateSchema, UserLoginSchema
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post(
    "/login",
    response_model=UserLoginSchema
)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return auth_service.login(
            username=body.username,
            password=body.password
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
