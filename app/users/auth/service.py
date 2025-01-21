import datetime
from dataclasses import dataclass
from datetime import timedelta

from jose import jwt
from jose.exceptions import JWTError

from app.users.auth.client import GoogleClient, YandexClient
from app.exception import (
    TokenNotCorrect,
    UserNotCorrectPasswordException,
    UserNotFoundException,
)
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema

from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)

        return UserLoginSchema(
            user_id=user.id,
            access_token=access_token
        )

    """
    Oauth email auth. Yandex and Google
    """

    async def auth_with_oauth(self, code: str, provider: str) -> UserLoginSchema:
        if provider == "google":
            user_data = await self.google_client.get_user_info(code=code)
            email = user_data.email
            access_token = user_data.access_token
        elif provider == "yandex":
            user_data = await self.yandex_client.get_user_info(code=code)
            email = user_data.default_email
            access_token = user_data.access_token
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        if user := await self.user_repository.get_user_by_mail(email=email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(
                user_id=user.id,
                access_token=access_token
            )

        create_user_data = UserCreateSchema(
            email=email,
            name=user_data.name,
            **{f"{provider}_access_token": access_token}
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)

        return UserLoginSchema(
            user_id=created_user.id,
            access_token=access_token
        )

    """
    Google auth/redirect methods
    """

    async def google_auth(self, code: str) -> UserLoginSchema:
        return await self.auth_with_oauth(code=code, provider='google')

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    """
    Yandex auth/redirect methods
    """

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        return await self.auth_with_oauth(code=code, provider='yandex')

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_data_unix = (datetime.datetime.utcnow() +
                             timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'exp': expires_data_unix},
                           self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY,
                                 algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect

        return payload["user_id"]
