from dataclasses import dataclass
from schema.user import UserLoginSchema, UserCreateSchema
from repository.user import UserRepository
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user_data_create = UserCreateSchema(username=username, password=password)
        user = await self.user_repository.create_user(user_data_create)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        print(user)
        return UserLoginSchema(
            user_id=user.id,
            access_token=access_token
        )
