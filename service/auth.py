from client import GoogleClient
from dataclasses import dataclass
import datetime
from datetime import timedelta

from exception import (
    UserNotFoundException,
    UserNotCorrectPasswordException,
    TokenNotCorrect,
)

from repository import UserRepository
from schema import UserLoginSchema, UserCreateSchema
from settings import Settings
from jose import jwt
from jose.exceptions import JWTError

from models.user import UserProfile


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)

        return UserLoginSchema(
            user_id=user.id,
            access_token=access_token
        )

    def google_auth(self, code: str) -> None:
        google_user_data = self.google_client.get_user_info(code=code)
        if user := self.user_repository.get_user_by_gmail(email=google_user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(
                user_id=created_user.id,
                access_token=access_token
            )
        print(google_user_data)
        create_user_data = UserCreateSchema(
            google_access_token=google_user_data.access_token,
            # email and name will be Null in our BD
            # if we login as a google user
            email=google_user_data.email,
            name=google_user_data.name
        )
        # no need to keep google access token in BD
        # at least in our case
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print(created_user)
        return UserLoginSchema(
            user_id=created_user.id,
            access_token=access_token
        )

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

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
