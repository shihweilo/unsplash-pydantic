"""Parameters documented by Unsplash that the client previously dropped."""

import httpx

from tests.test_models_minimal import MINIMAL_PHOTO
from unsplash import UnsplashClient


def test_search_photos_passes_lang(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/search/photos").mock(
        return_value=httpx.Response(
            200, json={"total": 0, "total_pages": 0, "results": []}
        )
    )

    with UnsplashClient(access_key="k") as client:
        client.search.photos("berg", lang="de", content_filter="high")

    params = dict(route.calls[0].request.url.params)
    assert params["lang"] == "de"
    assert params["content_filter"] == "high"


def test_random_passes_content_filter(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/photos/random").mock(
        return_value=httpx.Response(200, json=MINIMAL_PHOTO)
    )

    with UnsplashClient(access_key="k") as client:
        client.photos.random(query="nature", content_filter="high")

    params = dict(route.calls[0].request.url.params)
    assert params["content_filter"] == "high"
    assert params["query"] == "nature"


def test_user_statistics_passes_resolution_and_quantity(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/users/joe/statistics").mock(
        return_value=httpx.Response(200, json={"username": "joe"})
    )

    with UnsplashClient(access_key="k") as client:
        client.users.statistics("joe", resolution="days", quantity=90)

    assert dict(route.calls[0].request.url.params) == {
        "resolution": "days",
        "quantity": "90",
    }
