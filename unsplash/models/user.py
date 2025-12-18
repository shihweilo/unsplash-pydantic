from typing import Optional
from pydantic import HttpUrl
from ._base import UnsplashModel, Links

class UserProfileImage(UnsplashModel):
    small: HttpUrl
    medium: HttpUrl
    large: HttpUrl

class UserLinks(Links):
    photos: HttpUrl
    likes: HttpUrl
    portfolio: HttpUrl
    following: Optional[HttpUrl] = None
    followers: Optional[HttpUrl] = None

class User(UnsplashModel):
    id: str
    username: str
    name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    twitter_username: Optional[str] = None
    portfolio_url: Optional[HttpUrl] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    total_likes: int
    total_photos: int
    total_collections: int
    profile_image: UserProfileImage
    links: UserLinks
