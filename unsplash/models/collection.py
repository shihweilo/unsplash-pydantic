from datetime import datetime
from typing import Any, Optional

from pydantic import Field, HttpUrl

from ._base import Links, UnsplashModel
from .photo import Photo
from .user import User


class CollectionLinks(Links):
    """Only ``self`` and ``html`` (from :class:`Links`) are guaranteed."""

    photos: Optional[HttpUrl] = None
    related: Optional[HttpUrl] = None


class CollectionMeta(UnsplashModel):
    """SEO metadata attached to a collection."""

    title: Optional[str] = None
    description: Optional[str] = None
    index: Optional[bool] = None


class Collection(UnsplashModel):
    """
    A collection of photos.

    ``id``, ``title``, ``links`` and ``user`` are always present; timestamps
    and counters are optional because Unsplash omits them from abbreviated
    collection objects.
    """

    id: str
    title: str
    description: Optional[str] = None
    published_at: Optional[datetime] = None
    last_collected_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    featured: bool = False
    total_photos: Optional[int] = None
    total_plus: Optional[int] = None
    private: bool = False
    share_key: Optional[str] = None
    links: CollectionLinks
    user: User
    cover_photo: Optional[Photo] = None
    preview_photos: list[dict[str, Any]] = []
    meta: Optional[CollectionMeta] = None
    media_types: list[str] = Field(default_factory=list)
