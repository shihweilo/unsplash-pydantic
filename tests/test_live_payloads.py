"""
Regression tests against a real API response.

tests/fixtures/topic_wallpapers.json is a genuine GET /topics/wallpapers
response (repeated array entries trimmed, long strings shortened). Unlike
hand-written payloads it reflects what Unsplash actually sends, including
fields absent from the published documentation.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from unsplash.models import (
    Collection,
    CollectionLinks,
    CollectionMeta,
    HistoricalData,
    MonthStats,
    Photo,
    PhotoStatistics,
    Statistic,
    Topic,
    TotalStats,
    User,
    UserStatistics,
)

FIXTURES = Path(__file__).parent / "fixtures"
FIXTURE = FIXTURES / "topic_wallpapers.json"


@pytest.fixture
def payload():
    return json.loads(FIXTURE.read_text())


def test_topic_parses_live_response(payload):
    topic = Topic.model_validate(payload)
    assert topic.slug == "wallpapers"
    assert topic.media_types == ["photo"]
    assert topic.total_photos == 18071
    assert topic.cover_photo is not None
    assert topic.owners[0].username == "unsplash"


@pytest.mark.parametrize(
    "model,pointer",
    [
        (Topic, ()),
        (User, ("owners", 0)),
        (User, ("top_contributors", 0)),
        (User, ("top_contributors_last_30_days", 0)),
        (Photo, ("cover_photo",)),
    ],
)
def test_no_fields_are_silently_dropped(payload, model, pointer):
    """Every key Unsplash sends must map to a field, not vanish via extra='ignore'."""
    node = payload
    for step in pointer:
        node = node[step]
    unmapped = sorted(set(node) - set(model.model_fields))
    assert not unmapped, f"{model.__name__} drops {unmapped}"


def test_user_links_has_no_portfolio(payload):
    """
    Live responses omit links.portfolio entirely.

    This is the shape that raised a ValidationError before v0.3.0 and
    surfaced to users as a spurious OAuth error.
    """
    links = payload["owners"][0]["links"]
    assert "portfolio" not in links
    user = User.model_validate(payload["owners"][0])
    assert user.links is not None
    assert user.links.portfolio is None


def test_user_social_and_counters(payload):
    user = User.model_validate(payload["owners"][0])
    assert user.social is not None
    assert user.social.instagram_username == "unsplash"
    assert user.for_hire is False
    assert user.accepted_tos is True
    assert user.total_free_photos == 29
    assert user.total_illustrations == 0


def test_contributor_approved_submissions(payload):
    """Only present on top_contributors_last_30_days entries."""
    thirty_day = User.model_validate(payload["top_contributors_last_30_days"][0])
    owner = User.model_validate(payload["owners"][0])
    assert thirty_day.approved_submissions == 8
    assert owner.approved_submissions is None


def test_cover_photo_slugs_and_asset_type(payload):
    photo = Photo.model_validate(payload["cover_photo"])
    assert photo.slug == "glowing-abstract-flower--uCb8l4CMck"
    assert photo.alternative_slugs["en"].endswith("-uCb8l4CMck")
    assert photo.asset_type == "photo"
    assert photo.bookmarked is False
    assert photo.promoted_at is None


def test_cover_photo_topic_submissions(payload):
    photo = Photo.model_validate(payload["cover_photo"])
    submission = photo.topic_submissions["wallpapers"]
    assert submission.status == "approved"
    assert submission.approved_on is not None


def test_preview_photos_are_not_full_photos(payload):
    """
    preview_photos entries lack links, user and dimensions, so they cannot be
    parsed as Photo. This is why the field stays a list of dicts.
    """
    preview = payload["preview_photos"][0]
    assert "links" not in preview
    assert "user" not in preview
    with pytest.raises(ValidationError):
        Photo.model_validate(preview)


@pytest.mark.parametrize(
    "filename,model",
    [
        ("stats_total.json", TotalStats),
        ("stats_month.json", MonthStats),
        ("photo_statistics.json", PhotoStatistics),
        ("user_statistics.json", UserStatistics),
    ],
)
def test_stats_fixtures_map_every_key(filename, model):
    data = json.loads((FIXTURES / filename).read_text())
    model.model_validate(data)
    unmapped = sorted(set(data) - set(model.model_fields))
    assert not unmapped, f"{model.__name__} drops {unmapped}"


@pytest.mark.parametrize("filename", ["photo_statistics.json", "user_statistics.json"])
def test_nested_statistic_shapes_map_every_key(filename):
    data = json.loads((FIXTURES / filename).read_text())
    for key in ("downloads", "views"):
        node = data[key]
        assert not set(node) - set(Statistic.model_fields)
        assert not set(node["historical"]) - set(HistoricalData.model_fields)


def test_platform_totals():
    stats = TotalStats.model_validate(
        json.loads((FIXTURES / "stats_total.json").read_text())
    )
    assert stats.total_photos == 8764702
    assert stats.photo_downloads == 9232437914
    assert stats.requests == 0


def test_user_statistics_carries_id_and_username():
    stats = UserStatistics.model_validate(
        json.loads((FIXTURES / "user_statistics.json").read_text())
    )
    assert stats.id == "QV5S1rtoUJ0"
    assert stats.username == "unsplash"
    assert stats.downloads is not None
    assert stats.downloads.historical is not None
    assert stats.downloads.historical.average == 61
    assert str(stats.downloads.historical.values[0].date) == "2026-08-10"


def test_photo_statistics_carries_slug():
    stats = PhotoStatistics.model_validate(
        json.loads((FIXTURES / "photo_statistics.json").read_text())
    )
    assert stats.slug is not None
    assert stats.slug.endswith("-uCb8l4CMck")


# --- Collection ------------------------------------------------------------

COLLECTION = FIXTURES / "collection_star_wars.json"


@pytest.fixture
def collection_payload():
    return json.loads(COLLECTION.read_text())


def test_collection_parses_live_response(collection_payload):
    collection = Collection.model_validate(collection_payload)
    assert collection.id == "2423569"
    assert collection.title == "STAR WARS"
    assert collection.total_photos == 15
    assert collection.total_plus == 0
    assert collection.media_types == ["photo"]
    assert collection.cover_photo is not None
    assert collection.cover_photo.slug == "lego-star-wars-toy-i5Lmb7qPR7s"


def test_collection_meta(collection_payload):
    collection = Collection.model_validate(collection_payload)
    assert collection.meta is not None
    assert collection.meta.index is False
    assert collection.meta.title is None


@pytest.mark.parametrize(
    "model,pointer",
    [
        (Collection, ()),
        (CollectionLinks, ("links",)),
        (CollectionMeta, ("meta",)),
        (User, ("user",)),
        (Photo, ("cover_photo",)),
        (User, ("cover_photo", "user")),
    ],
)
def test_collection_drops_nothing(collection_payload, model, pointer):
    node = collection_payload
    for step in pointer:
        node = node[step]
    unmapped = sorted(set(node) - set(model.model_fields))
    assert not unmapped, f"{model.__name__} drops {unmapped}"


def test_collection_has_no_curated_or_tags(collection_payload):
    """
    Both were modelled but appear in neither live responses nor the docs;
    they were removed rather than left as fields that never populate.
    """
    assert "curated" not in collection_payload
    assert "tags" not in collection_payload
    assert "curated" not in Collection.model_fields
    assert "tags" not in Collection.model_fields
