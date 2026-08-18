import pytest

from unsplash import AsyncUnsplashClient, UnsplashClient


@pytest.fixture
def client():
    return UnsplashClient(access_key="test_key")


@pytest.fixture
async def async_client():
    async with AsyncUnsplashClient(access_key="test_key") as c:
        yield c
