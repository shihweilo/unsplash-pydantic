from datetime import datetime
from typing import Optional, List
from pydantic import HttpUrl
from ._base import UnsplashModel, Links
from .user import User
from .photo import Photo

class CollectionLinks(Links):
    photos: HttpUrl
    related: HttpUrl

class Collection(UnsplashModel):
    id: str
    title: str
    description: Optional[str] = None
    published_at: datetime
    last_collected_at: datetime
    updated_at: datetime
    curated: bool = False
    featured: bool = False
    total_photos: int
    private: bool = False
    share_key: Optional[str] = None
    tags: List[dict] = []
    links: CollectionLinks
    user: User
    cover_photo: Optional[Photo] = None
    preview_photos: List[dict] = []
