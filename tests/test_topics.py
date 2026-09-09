import httpx

from tests.test_models_minimal import MINIMAL_PHOTO
from unsplash import AsyncUnsplashClient, UnsplashClient

MINIMAL_TOPIC = {
    "id": "bo8jQKTaE0Y",
    "slug": "wallpapers",
    "title": "Wallpapers",
}

FULL_TOPIC = {
    **MINIMAL_TOPIC,
    "description": "From epic drone shots to inspiring moments in nature.",
    "published_at": "2020-04-17T02:31:04Z",
    "updated_at": "2020-06-09T22:35:11Z",
    "starts_at": "2020-04-01T00:00:00Z",
    "ends_at": None,
    "only_submissions_after": None,
    "visibility": "featured",
    "featured": True,
    "total_photos": 1000,
    "status": "open",
    "links": {
        "self": "https://api.unsplash.com/topics/wallpapers",
        "html": "https://unsplash.com/t/wallpapers",
        "photos": "https://api.unsplash.com/topics/wallpapers/photos",
    },
    "owners": [MINIMAL_PHOTO["user"]],
    "cover_photo": MINIMAL_PHOTO,
}


def test_list_topics(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/topics").mock(
        return_value=httpx.Response(200, json=[FULL_TOPIC])
    )

    with UnsplashClient(access_key="k") as client:
        topics = client.topics.list()

    assert [t.slug for t in topics] == ["wallpapers"]
    assert topics[0].featured is True
    assert topics[0].total_photos == 1000
    assert dict(route.calls[0].request.url.params) == {
        "page": "1",
        "per_page": "10",
        "order_by": "position",
    }


def test_list_topics_with_ids_and_order(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/topics").mock(
        return_value=httpx.Response(200, json=[])
    )

    with UnsplashClient(access_key="k") as client:
        client.topics.list(ids=["wallpapers", "nature"], order_by="featured")

    params = dict(route.calls[0].request.url.params)
    assert params["ids"] == "wallpapers,nature"
    assert params["order_by"] == "featured"


def test_get_topic_by_slug(respx_mock):
    respx_mock.get("https://api.unsplash.com/topics/wallpapers").mock(
        return_value=httpx.Response(200, json=FULL_TOPIC)
    )

    with UnsplashClient(access_key="k") as client:
        topic = client.topics.get("wallpapers")

    assert topic.id == "bo8jQKTaE0Y"
    assert topic.links is not None
    assert topic.cover_photo is not None
    assert topic.cover_photo.id == "Dwu85P9SOIk"
    assert topic.owners[0].username == "exampleuser"


def test_topic_photos(respx_mock):
    route = respx_mock.get("https://api.unsplash.com/topics/wallpapers/photos").mock(
        return_value=httpx.Response(200, json=[MINIMAL_PHOTO])
    )

    with UnsplashClient(access_key="k") as client:
        photos = client.topics.photos("wallpapers", orientation="landscape")

    assert [p.id for p in photos] == ["Dwu85P9SOIk"]
    params = dict(route.calls[0].request.url.params)
    assert params["orientation"] == "landscape"
    assert params["order_by"] == "latest"


def test_minimal_topic_parses(respx_mock):
    """A topic carrying only identity fields must not raise."""
    respx_mock.get("https://api.unsplash.com/topics/wallpapers").mock(
        return_value=httpx.Response(200, json=MINIMAL_TOPIC)
    )

    with UnsplashClient(access_key="k") as client:
        topic = client.topics.get("wallpapers")

    assert topic.links is None
    assert topic.cover_photo is None
    assert topic.owners == []
    assert topic.total_photos is None


async def test_async_topics(respx_mock):
    respx_mock.get("https://api.unsplash.com/topics").mock(
        return_value=httpx.Response(200, json=[FULL_TOPIC])
    )
    respx_mock.get("https://api.unsplash.com/topics/wallpapers/photos").mock(
        return_value=httpx.Response(200, json=[MINIMAL_PHOTO])
    )

    async with AsyncUnsplashClient(access_key="k") as client:
        topics = await client.topics.list()
        photos = await client.topics.photos("wallpapers")

    assert topics[0].slug == "wallpapers"
    assert photos[0].id == "Dwu85P9SOIk"
