from typing import Optional, TYPE_CHECKING, Dict, Any
from ..models import SearchResults, SearchUsersResults, SearchCollectionsResults

if TYPE_CHECKING:
    from .._client_base import HTTPClient, AsyncHTTPClient

class SearchResource:
    """Handle search endpoints."""
    
    def __init__(self, client: "HTTPClient"):
        self._client = client

    def photos(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10,
        orientation: Optional[str] = None,
        color: Optional[str] = None,
        order_by: Optional[str] = None,
        collections: Optional[str] = None,
        content_filter: Optional[str] = None
    ) -> SearchResults:
        """Search photos."""
        params: Dict[str, Any] = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        if orientation: params["orientation"] = orientation
        if color: params["color"] = color
        if order_by: params["order_by"] = order_by
        if collections: params["collections"] = collections
        if content_filter: params["content_filter"] = content_filter

        response = self._client.request("GET", "/search/photos", params=params)
        return SearchResults.model_validate(response.json())

    def users(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10
    ) -> SearchUsersResults:
        """Search users."""
        params: Dict[str, Any] = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        response = self._client.request("GET", "/search/users", params=params)
        return SearchUsersResults.model_validate(response.json())

    def collections(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10
    ) -> SearchCollectionsResults:
        """Search collections."""
        params: Dict[str, Any] = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        response = self._client.request("GET", "/search/collections", params=params)
        return SearchCollectionsResults.model_validate(response.json())


class AsyncSearchResource:
    """Async handle search endpoints."""
    
    def __init__(self, client: "AsyncHTTPClient"):
        self._client = client

    async def photos(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10,
        orientation: Optional[str] = None,
        color: Optional[str] = None,
        order_by: Optional[str] = None,
        collections: Optional[str] = None,
        content_filter: Optional[str] = None
    ) -> SearchResults:
        """Search photos."""
        params: Dict[str, Any] = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        if orientation: params["orientation"] = orientation
        if color: params["color"] = color
        if order_by: params["order_by"] = order_by
        if collections: params["collections"] = collections
        if content_filter: params["content_filter"] = content_filter

        response = await self._client.request("GET", "/search/photos", params=params)
        return SearchResults.model_validate(response.json())

    async def users(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10
    ) -> SearchUsersResults:
        """Search users."""
        params: Dict[str, Any] = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        response = await self._client.request("GET", "/search/users", params=params)
        return SearchUsersResults.model_validate(response.json())

    async def collections(
        self,
        query: str,
        page: int = 1,
        per_page: int = 10
    ) -> SearchCollectionsResults:
        """Search collections."""
        params: Dict[str, Any] = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        response = await self._client.request("GET", "/search/collections", params=params)
        return SearchCollectionsResults.model_validate(response.json())
