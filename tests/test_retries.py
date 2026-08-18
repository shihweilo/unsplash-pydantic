import httpx
import pytest

from unsplash import AsyncUnsplashClient, RateLimitError, UnsplashClient, UnsplashError
from unsplash._client_base import _backoff_delay, _parse_retry_after, _retry_delay


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    """Keep retry tests fast; record the delays that would have been slept."""
    slept = []
    monkeypatch.setattr("unsplash._client_base.time.sleep", slept.append)

    async def _async_sleep(delay):
        slept.append(delay)

    monkeypatch.setattr("unsplash._client_base.asyncio.sleep", _async_sleep)
    return slept


PHOTO = {
    "id": "foo",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "width": 100,
    "height": 100,
    "likes": 0,
    "urls": {
        "raw": "http://e.com/raw",
        "full": "http://e.com/full",
        "regular": "http://e.com/reg",
        "small": "http://e.com/small",
        "thumb": "http://e.com/thumb",
    },
    "links": {
        "self": "http://e.com",
        "html": "http://e.com",
        "download": "http://e.com/dl",
        "download_location": "http://e.com/dl_loc",
    },
    "user": {
        "id": "u1",
        "username": "u1",
        "name": "User 1",
        "total_likes": 0,
        "total_photos": 0,
        "total_collections": 0,
        "profile_image": {
            "small": "http://e.com/s",
            "medium": "http://e.com/m",
            "large": "http://e.com/l",
        },
        "links": {
            "self": "http://e.com",
            "html": "http://e.com",
            "photos": "http://e.com",
            "likes": "http://e.com",
            "portfolio": "http://e.com",
        },
    },
}


def test_retries_5xx_then_succeeds(respx_mock, no_sleep):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(502),
            httpx.Response(200, json=PHOTO),
        ]
    )

    with UnsplashClient(access_key="k") as client:
        photo = client.photos.get("foo")

    assert photo.id == "foo"
    assert route.call_count == 3
    assert no_sleep == [0.5, 1.0]  # exponential backoff between attempts


def test_retry_budget_is_exhausted_then_raises(respx_mock, no_sleep):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        return_value=httpx.Response(503)
    )

    with UnsplashClient(access_key="k", max_retries=2) as client:
        with pytest.raises(UnsplashError) as exc_info:
            client.photos.get("foo")

    assert exc_info.value.http_status == 503
    assert route.call_count == 3  # 1 initial attempt + 2 retries


def test_max_retries_zero_disables_retrying(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        return_value=httpx.Response(503)
    )

    with UnsplashClient(access_key="k", max_retries=0) as client:
        with pytest.raises(UnsplashError):
            client.photos.get("foo")

    assert route.call_count == 1


def test_negative_max_retries_rejected():
    with pytest.raises(ValueError, match="max_retries must be >= 0"):
        UnsplashClient(access_key="k", max_retries=-1)


def test_404_is_not_retried(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        return_value=httpx.Response(404, json={"errors": ["Not Found"]})
    )

    with UnsplashClient(access_key="k") as client:
        with pytest.raises(UnsplashError):
            client.photos.get("foo")

    assert route.call_count == 1


def test_429_without_retry_after_is_not_retried(respx_mock):
    """Unsplash's quota is hourly, so a bare 429 should fail fast."""
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        return_value=httpx.Response(
            429,
            json={"errors": ["Rate Limit Exceeded"]},
            headers={"X-Ratelimit-Limit": "50", "X-Ratelimit-Remaining": "0"},
        )
    )

    with UnsplashClient(access_key="k") as client:
        with pytest.raises(RateLimitError) as exc_info:
            client.photos.get("foo")

    assert route.call_count == 1
    assert exc_info.value.limit == 50
    assert exc_info.value.remaining == 0


def test_429_with_short_retry_after_is_retried(respx_mock, no_sleep):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "2"}),
            httpx.Response(200, json=PHOTO),
        ]
    )

    with UnsplashClient(access_key="k") as client:
        photo = client.photos.get("foo")

    assert photo.id == "foo"
    assert route.call_count == 2
    assert no_sleep == [2.0]  # honors the server's delay, not our backoff


def test_429_with_long_retry_after_fails_fast(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        return_value=httpx.Response(429, headers={"Retry-After": "3600"})
    )

    with UnsplashClient(access_key="k") as client:
        with pytest.raises(RateLimitError):
            client.photos.get("foo")

    assert route.call_count == 1


def test_transport_errors_are_retried(respx_mock, no_sleep):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        side_effect=[
            httpx.ConnectError("boom"),
            httpx.ReadTimeout("slow"),
            httpx.Response(200, json=PHOTO),
        ]
    )

    with UnsplashClient(access_key="k") as client:
        photo = client.photos.get("foo")

    assert photo.id == "foo"
    assert route.call_count == 3


def test_transport_error_propagates_when_budget_exhausted(respx_mock, no_sleep):
    respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        side_effect=httpx.ConnectError("boom")
    )

    with UnsplashClient(access_key="k", max_retries=1) as client:
        with pytest.raises(httpx.ConnectError):
            client.photos.get("foo")


async def test_async_client_retries_5xx(respx_mock, no_sleep):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        side_effect=[httpx.Response(500), httpx.Response(200, json=PHOTO)]
    )

    async with AsyncUnsplashClient(access_key="k") as client:
        photo = await client.photos.get("foo")

    assert photo.id == "foo"
    assert route.call_count == 2
    assert no_sleep == [0.5]


async def test_async_transport_errors_are_retried(respx_mock, no_sleep):
    route = respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        side_effect=[httpx.ConnectError("boom"), httpx.Response(200, json=PHOTO)]
    )

    async with AsyncUnsplashClient(access_key="k") as client:
        photo = await client.photos.get("foo")

    assert photo.id == "foo"
    assert route.call_count == 2


@pytest.mark.parametrize(
    "header,expected",
    [(None, None), ("", None), ("5", 5.0), ("0", 0.0), ("not-a-number", None)],
)
def test_parse_retry_after(header, expected):
    assert _parse_retry_after(header) == expected


def test_parse_retry_after_http_date():
    # A date in the past clamps to 0 rather than going negative.
    assert _parse_retry_after("Wed, 21 Oct 2015 07:28:00 GMT") == 0.0


def test_backoff_is_capped():
    assert _backoff_delay(0) == 0.5
    assert _backoff_delay(1) == 1.0
    assert _backoff_delay(100) == 30.0


def test_success_is_never_retried():
    assert _retry_delay(httpx.Response(200), 0) is None
