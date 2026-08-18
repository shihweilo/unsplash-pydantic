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


class Photo(UnsplashModel):
    """
    A photo.

    ``id`` and ``urls`` are always present. The remaining core fields
    (``links``, ``user``, dimensions) are present on every photo this client
    returns, but counters and timestamps that Unsplash omits from abbreviated
    responses are optional.
    """

    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    width: int
    height: int
    color: Optional[str] = None
    blur_hash: Optional[str] = None
    description: Optional[str] = None
    alt_description: Optional[str] = None
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
