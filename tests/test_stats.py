import httpx

from unsplash import AsyncUnsplashClient, UnsplashClient

PHOTO_STATS = {
    "id": "Dwu85P9SOIk",
    "downloads": {
        "total": 6303,
        "historical": {
            "change": 460,
            "average": 15,
            "resolution": "days",
            "quantity": 30,
            "values": [{"date": "2017-02-27", "value": 44}],
        },
    },
    "views": {"total": 1075533, "historical": {"change": 45856}},
    "likes": {"total": 40},
}

USER_STATS = {
    "username": "exampleuser",
    "downloads": {"total": 15687, "historical": {"change": 608, "quantity": 30}},
    "views": {"total": 2545809},
}


def test_photo_statistics(respx_mock):
    route = respx_mock.get(
        "https://api.unsplash.com/photos/Dwu85P9SOIk/statistics"
    ).mock(return_value=httpx.Response(200, json=PHOTO_STATS))

    with UnsplashClient(access_key="k") as client:
        stats = client.photos.statistics("Dwu85P9SOIk", resolution="days", quantity=7)

    assert stats.downloads is not None
    assert stats.downloads.total == 6303
    assert stats.downloads.historical is not None
    assert stats.downloads.historical.values[0].value == 44
    assert str(stats.downloads.historical.values[0].date) == "2017-02-27"
    assert dict(route.calls[0].request.url.params) == {
        "resolution": "days",
        "quantity": "7",
    }


def test_user_statistics_is_typed(respx_mock):
    respx_mock.get("https://api.unsplash.com/users/exampleuser/statistics").mock(
        return_value=httpx.Response(200, json=USER_STATS)
    )

    with UnsplashClient(access_key="k") as client:
        stats = client.users.statistics("exampleuser")

    assert stats.username == "exampleuser"
    assert stats.downloads is not None
    assert stats.downloads.total == 15687
    assert stats.likes is None


def test_stats_total(respx_mock):
    respx_mock.get("https://api.unsplash.com/stats/total").mock(
        return_value=httpx.Response(
            200,
            json={
                "total_photos": 209824,
                "photo_downloads": 1120271133,
                "views": 100,
                "photographers": 5,
            },
        )
    )

    with UnsplashClient(access_key="k") as client:
        stats = client.stats.total()

    assert stats.total_photos == 209824
    assert stats.photographers == 5
    assert stats.downloads is None  # absent key stays None, unknown keys ignored


def test_stats_month(respx_mock):
    respx_mock.get("https://api.unsplash.com/stats/month").mock(
        return_value=httpx.Response(
            200, json={"downloads": 100, "views": 200, "new_photos": 30}
        )
    )

    with UnsplashClient(access_key="k") as client:
        stats = client.stats.month()

    assert stats.downloads == 100
    assert stats.new_photos == 30


def test_empty_statistics_payload_does_not_raise(respx_mock):
    respx_mock.get("https://api.unsplash.com/stats/total").mock(
        return_value=httpx.Response(200, json={})
    )

    with UnsplashClient(access_key="k") as client:
        assert client.stats.total().total_photos is None


async def test_async_stats(respx_mock):
    respx_mock.get("https://api.unsplash.com/stats/month").mock(
        return_value=httpx.Response(200, json={"downloads": 7})
    )
    respx_mock.get("https://api.unsplash.com/photos/abc/statistics").mock(
        return_value=httpx.Response(200, json=PHOTO_STATS)
    )

    async with AsyncUnsplashClient(access_key="k") as client:
        month = await client.stats.month()
        photo = await client.photos.statistics("abc")

    assert month.downloads == 7
    assert photo.likes is not None
    assert photo.likes.total == 40
