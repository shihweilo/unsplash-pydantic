from ._base import UnsplashModel
from .collection import Collection
from .photo import Photo
from .user import User


class SearchResults(UnsplashModel):
    total: int
    total_pages: int
    results: list[Photo]


class SearchUsersResults(UnsplashModel):
    total: int
    total_pages: int
    results: list[User]


class SearchCollectionsResults(UnsplashModel):
    total: int
    total_pages: int
    results: list[Collection]
