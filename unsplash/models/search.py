from typing import List, Generic, TypeVar
from ._base import UnsplashModel
from .photo import Photo
from .user import User
from .collection import Collection

class SearchResults(UnsplashModel):
    total: int
    total_pages: int
    results: List[Photo]

class SearchUsersResults(UnsplashModel):
    total: int
    total_pages: int
    results: List[User]

class SearchCollectionsResults(UnsplashModel):
    total: int
    total_pages: int
    results: List[Collection]
