from datetime import datetime
from typing import Any, Optional

from pydantic import Field, HttpUrl

from ._base import Links, UnsplashModel
from .user import User


class PhotoUrls(UnsplashModel):
    raw: HttpUrl
    full: HttpUrl
    regular: HttpUrl
    small: HttpUrl
    thumb: HttpUrl
    small_s3: Optional[HttpUrl] = None


class PhotoLinks(Links):
    download: Optional[HttpUrl] = None
    download_location: Optional[HttpUrl] = None


class Exif(UnsplashModel):
    make: Optional[str] = None
    model: Optional[str] = None
    name: Optional[str] = None
    exposure_time: Optional[str] = None
    aperture: Optional[str] = None
    focal_length: Optional[str] = None
    iso: Optional[int] = None


class LocationPosition(UnsplashModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Location(UnsplashModel):
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    position: Optional[LocationPosition] = None


class TopicSubmission(UnsplashModel):
    """Status of a photo's submission to a topic."""

    status: Optional[str] = None
    approved_on: Optional[datetime] = None


class Photo(UnsplashModel):
    """
    A photo.

    ``id`` and ``urls`` are always present. The remaining core fields
    (``links``, ``user``, dimensions) are present on every photo this client
    returns, but counters and timestamps that Unsplash omits from abbreviated
    responses are optional.
    """

    id: str
    slug: Optional[str] = None
    alternative_slugs: dict[str, str] = Field(default_factory=dict)
    asset_type: Optional[str] = None
    created_at: datetime
    promoted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    width: int
    height: int
    color: Optional[str] = None
    blur_hash: Optional[str] = None
    description: Optional[str] = None
    alt_description: Optional[str] = None
    short_description: Optional[str] = None
    urls: PhotoUrls
    links: PhotoLinks
    likes: Optional[int] = None
    liked_by_user: bool = False
    user: User
    current_user_collections: list[dict[str, Any]] = Field(default_factory=list)
    sponsorship: Optional[dict[str, Any]] = None
    exif: Optional[Exif] = None
    location: Optional[Location] = None
    views: Optional[int] = None
    downloads: Optional[int] = None
    topics: list[dict[str, Any]] = Field(default_factory=list)
    topic_submissions: dict[str, TopicSubmission] = Field(default_factory=dict)
    breadcrumbs: list[dict[str, Any]] = Field(default_factory=list)
    bookmarked: Optional[bool] = None
