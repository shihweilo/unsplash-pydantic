from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import HttpUrl, Field
from ._base import UnsplashModel, Links
from .user import User

class PhotoUrls(UnsplashModel):
    raw: HttpUrl
    full: HttpUrl
    regular: HttpUrl
    small: HttpUrl
    thumb: HttpUrl
    small_s3: Optional[HttpUrl] = None

class PhotoLinks(Links):
    download: HttpUrl
    download_location: HttpUrl

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
    id: str
    created_at: datetime
    updated_at: datetime
    width: int
    height: int
    color: Optional[str] = None
    blur_hash: Optional[str] = None
    description: Optional[str] = None
    alt_description: Optional[str] = None
    urls: PhotoUrls
    links: PhotoLinks
    likes: int
    liked_by_user: bool = False
    user: User
    current_user_collections: List[Dict[str, Any]] = Field(default_factory=list)
    sponsorship: Optional[Dict[str, Any]] = None
    exif: Optional[Exif] = None
    location: Optional[Location] = None
    views: Optional[int] = None
    downloads: Optional[int] = None
    topics: List[Dict[str, Any]] = Field(default_factory=list)
