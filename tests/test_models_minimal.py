"""
Regression tests for abbreviated API payloads.

Unsplash returns trimmed objects when a resource is embedded in another
(a user inside a photo, a cover photo inside a collection). Requiring a field
that Unsplash omits raises a pydantic ValidationError from deep inside the
client, which historically surfaced to users as a confusing "OAuth error"
(see the v0.2.1 UserLinks fix). Each test here parses the *minimum* documented
shape, so tightening a field again fails loudly.
"""

from unsplash.models import Collection, Photo, User

# The user object as documented inside a "Get a photo" response: no
# profile_image, no total_likes/total_photos, and links carrying only
# self/html/photos.
EMBEDDED_USER = {
    "id": "QPxL2MGqfrw",
    "username": "exampleuser",
    "name": "Joe Example",
    "portfolio_url": None,
    "bio": None,
    "location": None,
    "total_collections": 13,
    "links": {
        "self": "https://api.unsplash.com/users/exampleuser",
        "html": "https://unsplash.com/exampleuser",
        "photos": "https://api.unsplash.com/users/exampleuser/photos",
    },
}

MINIMAL_PHOTO = {
    "id": "Dwu85P9SOIk",
    "created_at": "2016-05-03T11:00:28-04:00",
    "width": 2448,
    "height": 3264,
    "urls": {
        "raw": "https://images.unsplash.com/photo-1417325384643",
        "full": "https://images.unsplash.com/photo-1417325384643?q=75",
        "regular": "https://images.unsplash.com/photo-1417325384643?w=1080",
        "small": "https://images.unsplash.com/photo-1417325384643?w=400",
        "thumb": "https://images.unsplash.com/photo-1417325384643?w=200",
    },
    "links": {
        "self": "https://api.unsplash.com/photos/Dwu85P9SOIk",
        "html": "https://unsplash.com/photos/Dwu85P9SOIk",
    },
    "user": EMBEDDED_USER,
}


def test_user_parses_with_only_id_and_username():
    user = User.model_validate({"id": "abc", "username": "someone"})
    assert user.id == "abc"
    assert user.name is None
    assert user.profile_image is None
    assert user.links is None
    assert user.total_photos is None


def test_embedded_user_without_profile_image_or_totals():
    """The exact shape Unsplash documents inside a photo response."""
    user = User.model_validate(EMBEDDED_USER)
    assert user.username == "exampleuser"
    assert user.profile_image is None
    assert user.total_likes is None
    assert user.total_photos is None
    assert user.total_collections == 13


def test_user_links_without_likes_or_portfolio():
    """Regression for the v0.2.1 class of bug, extended to likes/portfolio."""
    user = User.model_validate(EMBEDDED_USER)
    assert user.links is not None
    assert user.links.photos is not None
    assert user.links.likes is None
    assert user.links.portfolio is None
    assert user.links.following is None
    assert user.links.followers is None


def test_photo_parses_without_optional_counters():
    photo = Photo.model_validate(MINIMAL_PHOTO)
    assert photo.id == "Dwu85P9SOIk"
    assert str(photo.urls.full).startswith("https://images.unsplash.com/")
    assert photo.updated_at is None
    assert photo.likes is None
    assert photo.exif is None
    assert photo.location is None


def test_photo_links_without_download_urls():
    photo = Photo.model_validate(MINIMAL_PHOTO)
    assert photo.links.download is None
    assert photo.links.download_location is None


def test_photo_embedded_user_is_still_usable():
    """The primary access path in the README must survive an abbreviated user."""
    photo = Photo.model_validate(MINIMAL_PHOTO)
    assert photo.user.name == "Joe Example"
    assert photo.user.profile_image is None


def test_collection_parses_without_timestamps_or_counters():
    collection = Collection.model_validate(
        {
            "id": "296",
            "title": "I like a man with a beard.",
            "links": {
                "self": "https://api.unsplash.com/collections/296",
                "html": "https://unsplash.com/collections/296",
            },
            "user": EMBEDDED_USER,
        }
    )
    assert collection.id == "296"
    assert collection.published_at is None
    assert collection.last_collected_at is None
    assert collection.total_photos is None
    assert collection.cover_photo is None


def test_collection_with_abbreviated_cover_photo():
    collection = Collection.model_validate(
        {
            "id": "296",
            "title": "Beards",
            "links": {
                "self": "https://api.unsplash.com/collections/296",
                "html": "https://unsplash.com/collections/296",
            },
            "user": EMBEDDED_USER,
            "cover_photo": MINIMAL_PHOTO,
        }
    )
    assert collection.cover_photo is not None
    assert collection.cover_photo.id == "Dwu85P9SOIk"
