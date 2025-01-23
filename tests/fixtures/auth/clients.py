from dataclasses import dataclass

import httpx
import pytest

from faker import Factory as FakerFactory

from app.users.auth.schema import GoogleUserData
from settings import Settings

faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code=code)
        return {"fake_access_token": access_token}

    @staticmethod
    async def _get_user_access_token(code: str) -> str:
        return f"fake_access_token_{code}"


@dataclass
class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code=code)
        return {"fake_access_token": access_token}

    @staticmethod
    async def _get_user_access_token(code: str) -> str:
        return f"fake_access_token_{code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(
        settings=Settings(),
        async_client=httpx.AsyncClient(),
    )


@pytest.fixture
def yandex_client():
    return FakeYandexClient(
        settings=Settings(),
        async_client=httpx.AsyncClient(),
    )


@pytest.fixture
def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=faker.random_int(),
        email=faker.email(),
        name=faker.name(),
        verified_email=True,
        access_token=faker.sha256(),

    )
