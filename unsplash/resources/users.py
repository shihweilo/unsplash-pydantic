from typing import List, Optional, Union, TYPE_CHECKING, Dict, Any, cast
from ..models import User, Photo, Collection

if TYPE_CHECKING:
    from .._client_base import HTTPClient, AsyncHTTPClient

class UsersResource:
    """Handle user-related endpoints."""
    
    def __init__(self, client: "HTTPClient"):
        self._client = client
    
    def get(self, username: str) -> User:
        """Get public details on a user."""
        response = self._client.request("GET", f"/users/{username}")
        return User.model_validate(response.json())
    
    def portfolio(self, username: str) -> str:
        """Retrieve a user's portfolio link."""
        response = self._client.request("GET", f"/users/{username}/portfolio")
        return str(response.json()["url"])
        
    def photos(
        self,
        username: str,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "latest",
        stats: bool = False,
        resolution: str = "days",
        quantity: int = 30,
        orientation: Optional[str] = None
    ) -> List[Photo]:
        """Get a user's photos."""
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order_by": order_by,
            "stats": str(stats).lower()
        }
        if stats:
            params["resolution"] = resolution
            params["quantity"] = quantity
        if orientation:
            params["orientation"] = orientation
            
        response = self._client.request("GET", f"/users/{username}/photos", params=params)
        return [Photo.model_validate(item) for item in response.json()]
    
    def likes(
        self,
        username: str,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "latest",
        orientation: Optional[str] = None
    ) -> List[Photo]:
        """Get a user's liked photos."""
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order_by": order_by
        }
        if orientation:
            params["orientation"] = orientation

        response = self._client.request("GET", f"/users/{username}/likes", params=params)
        return [Photo.model_validate(item) for item in response.json()]
    
    def collections(
        self,
        username: str,
        page: int = 1,
        per_page: int = 10
    ) -> List[Collection]:
        """Get a user's collections."""
        params = {
            "page": page,
            "per_page": per_page
        }
        response = self._client.request("GET", f"/users/{username}/collections", params=params)
        return [Collection.model_validate(item) for item in response.json()]

    def statistics(self, username: str) -> Dict[str, Any]: # TODO: Define Statistics model if needed
        """Get a user's statistics."""
        response = self._client.request("GET", f"/users/{username}/statistics")
        return cast(Dict[str, Any], response.json())


class AsyncUsersResource:
    """Async handle user-related endpoints."""
    
    def __init__(self, client: "AsyncHTTPClient"):
        self._client = client
    
    async def get(self, username: str) -> User:
        """Get public details on a user."""
        response = await self._client.request("GET", f"/users/{username}")
        return User.model_validate(response.json())
    
    async def portfolio(self, username: str) -> str:
        """Retrieve a user's portfolio link."""
        response = await self._client.request("GET", f"/users/{username}/portfolio")
        return str(response.json()["url"])
        
    async def photos(
        self,
        username: str,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "latest",
        stats: bool = False,
        resolution: str = "days",
        quantity: int = 30,
        orientation: Optional[str] = None
    ) -> List[Photo]:
        """Get a user's photos."""
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order_by": order_by,
            "stats": str(stats).lower()
        }
        if stats:
            params["resolution"] = resolution
            params["quantity"] = quantity
        if orientation:
            params["orientation"] = orientation
            
        response = await self._client.request("GET", f"/users/{username}/photos", params=params)
        return [Photo.model_validate(item) for item in response.json()]
    
    async def likes(
        self,
        username: str,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "latest",
        orientation: Optional[str] = None
    ) -> List[Photo]:
        """Get a user's liked photos."""
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order_by": order_by
        }
        if orientation:
            params["orientation"] = orientation

        response = await self._client.request("GET", f"/users/{username}/likes", params=params)
        return [Photo.model_validate(item) for item in response.json()]
    
    async def collections(
        self,
        username: str,
        page: int = 1,
        per_page: int = 10
    ) -> List[Collection]:
        """Get a user's collections."""
        params = {
            "page": page,
            "per_page": per_page
        }
        response = await self._client.request("GET", f"/users/{username}/collections", params=params)
        return [Collection.model_validate(item) for item in response.json()]

    async def statistics(self, username: str) -> Dict[str, Any]: # TODO: Define Statistics model if needed
        """Get a user's statistics."""
        response = await self._client.request("GET", f"/users/{username}/statistics")
        return cast(Dict[str, Any], response.json())
