from typing import Optional

from pydantic import HttpUrl

from ._base import Links, UnsplashModel


class UserProfileImage(UnsplashModel):
    small: HttpUrl
    medium: HttpUrl
    large: HttpUrl


class UserLinks(Links):
    """
    Links on a user object.

    Only ``self`` and ``html`` (inherited from :class:`Links`) are guaranteed.
    Unsplash abbreviates this object when a user is embedded in another
    resource -- an embedded user's links may carry nothing but ``self``,
    ``html`` and ``photos``.
    """

    photos: Optional[HttpUrl] = None
    likes: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None
    following: Optional[HttpUrl] = None
    followers: Optional[HttpUrl] = None


class User(UnsplashModel):
    """
    An Unsplash user.

    Only ``id`` and ``username`` are guaranteed. Unsplash returns abbreviated
    user objects when a user is embedded in a photo or collection, omitting
    ``profile_image`` and some of the ``total_*`` counters, so every other
    field is optional. Check for ``None`` before use.
    """

    id: str
    username: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    instagram_username: Optional[str] = None
    twitter_username: Optional[str] = None
    portfolio_url: Optional[HttpUrl] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    total_likes: Optional[int] = None
    total_photos: Optional[int] = None
    total_collections: Optional[int] = None
    profile_image: Optional[UserProfileImage] = None
    links: Optional[UserLinks] = None
