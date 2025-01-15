from dataclasses import dataclass

from schema import UserCreateSchema
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models import UserProfile


@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump()).returning(UserProfile.id)

        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            session.flush()
            return self.get_user(user_id)

    def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            # with scalar_one_or_none we are return user object
            # or none if user_id doesn't exists
            user = session.execute(query).scalar_one_or_none()
            return user

    def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session() as session:
            user = session.execute(query).scalar_one_or_none()
            return user

    def get_user_by_mail(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.email == email)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()
