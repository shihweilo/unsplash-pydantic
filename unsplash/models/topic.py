from datetime import datetime
from typing import Any, Optional

from pydantic import Field, HttpUrl

from ._base import Links, UnsplashModel
from .photo import Photo
from .user import User


class TopicLinks(Links):
    """Only ``self`` and ``html`` (from :class:`Links`) are guaranteed."""

    photos: Optional[HttpUrl] = None


class Topic(UnsplashModel):
    """
    An editorial topic.

    Following the convention used by the other models, only identity fields
    are required; everything Unsplash may omit from an abbreviated topic
    object is optional.
    """

    id: str
    slug: str
    title: str
    description: Optional[str] = None
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    only_submissions_after: Optional[datetime] = None
    visibility: Optional[str] = None
    featured: bool = False
    total_photos: Optional[int] = None
    status: Optional[str] = None
    media_types: list[str] = Field(default_factory=list)
    links: Optional[TopicLinks] = None
    owners: list[User] = Field(default_factory=list)
    top_contributors: list[User] = Field(default_factory=list)
    top_contributors_last_30_days: list[User] = Field(default_factory=list)
    cover_photo: Optional[Photo] = None
    preview_photos: list[dict[str, Any]] = Field(default_factory=list)
    current_user_contributions: list[dict[str, Any]] = Field(default_factory=list)
    total_current_user_submissions: Optional[int] = None
