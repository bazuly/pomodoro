import pytest

from settings import Settings


@pytest.fixture
def settings():
    return Settings()
