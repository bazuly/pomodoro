import datetime as dt

import pytest
from jose import jwt

from app.users.auth.service import AuthService
from settings import Settings

pytestmark = pytest.mark.asyncio


def test_get_google_redirect__success(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url

    auth_service_google_redirect_url = auth_service.get_google_redirect_url()

    assert auth_service_google_redirect_url == settings_google_redirect_url


def test_get_yandex_redirect__success(auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url

    auth_service_yandex_redirect_url = auth_service.get_yandex_redirect_url()

    assert auth_service_yandex_redirect_url == settings_yandex_redirect_url


def test_get_google_redirect__failure(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = "https://fake-redirect-url.com"

    auth_service_google_redirect_url = auth_service.get_google_redirect_url()

    assert auth_service_google_redirect_url != settings_google_redirect_url


def test_get_yandex_redirect__failure(auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = "https://fake-redirect-url.com"

    auth_service_yandex_redirect_url = auth_service.get_yandex_redirect_url()

    assert auth_service_yandex_redirect_url != settings_yandex_redirect_url


async def test_generate_access_token__success(auth_service: AuthService, settings: Settings):
    user_id = 1

    access_token = auth_service.generate_access_token(user_id=user_id)
    decode_access_token = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[
        settings.JWT_ENCODE_ALGORITHM])
    decode_user_id = decode_access_token.get("user_id")
    decode_token_expire = dt.datetime.fromtimestamp(
        decode_access_token.get("exp"), tz=dt.timezone.utc)

    assert (decode_token_expire - dt.datetime.now(tz=dt.UTC)
            ) > dt.timedelta(days=6)
    assert user_id == decode_user_id


async def test_get_user_id_from_access_token__success(auth_service: AuthService):
    user_id = 1

    access_token = auth_service.generate_access_token(user_id=user_id)
    decode_user_id = auth_service.get_user_id_from_access_token(access_token)
    assert user_id == decode_user_id

# need to fix later
# AttributeError: 'dict' object has no attribute 'email'
# async def test_google_auth__success(auth_service: AuthService):
#     code = "fake_code"
#
#     user = await auth_service.google_auth(code=code)
#     decode_user_id = auth_service.get_user_id_from_access_token(user.access_token)
#     assert user.user_id == decode_user_id
#     assert isinstance(user, UserLoginSchema)
