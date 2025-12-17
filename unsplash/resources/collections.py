from typing import List, Optional, TYPE_CHECKING, Dict, Any
from ..models import Collection, Photo

if TYPE_CHECKING:
    from .._client_base import HTTPClient, AsyncHTTPClient

class CollectionsResource:
    """Handle collection-related endpoints."""
    
    def __init__(self, client: "HTTPClient"):
        self._client = client
    
    def get(self, collection_id: str) -> Collection:
        """Get a single collection."""
        response = self._client.request("GET", f"/collections/{collection_id}")
        return Collection.model_validate(response.json())
    
    def list(
        self,
        page: int = 1,
        per_page: int = 10
    ) -> List[Collection]:
        """List all collections."""
        response = self._client.request(
            "GET",
            "/collections",
            params={"page": page, "per_page": per_page}
        )
        return [Collection.model_validate(item) for item in response.json()]
    
    def photos(
        self,
        collection_id: str,
        page: int = 1,
        per_page: int = 10,
        orientation: Optional[str] = None
    ) -> List[Photo]:
        """Get photos from a collection."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if orientation:
            params["orientation"] = orientation
            
        response = self._client.request(
            "GET",
            f"/collections/{collection_id}/photos",
            params=params
        )
        return [Photo.model_validate(item) for item in response.json()]

    def related(self, collection_id: str) -> List[Collection]:
        """Get related collections."""
        response = self._client.request("GET", f"/collections/{collection_id}/related")
        return [Collection.model_validate(item) for item in response.json()]


class AsyncCollectionsResource:
    """Async handle collection-related endpoints."""
    
    def __init__(self, client: "AsyncHTTPClient"):
        self._client = client
    
    async def get(self, collection_id: str) -> Collection:
        """Get a single collection."""
        response = await self._client.request("GET", f"/collections/{collection_id}")
        return Collection.model_validate(response.json())
    
    async def list(
        self,
        page: int = 1,
        per_page: int = 10
    ) -> List[Collection]:
        """List all collections."""
        response = await self._client.request(
            "GET",
            "/collections",
            params={"page": page, "per_page": per_page}
        )
        return [Collection.model_validate(item) for item in response.json()]
    
    async def photos(
        self,
        collection_id: str,
        page: int = 1,
        per_page: int = 10,
        orientation: Optional[str] = None
    ) -> List[Photo]:
        """Get photos from a collection."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if orientation:
            params["orientation"] = orientation
            
        response = await self._client.request(
            "GET",
            f"/collections/{collection_id}/photos",
            params=params
        )
        return [Photo.model_validate(item) for item in response.json()]

    async def related(self, collection_id: str) -> List[Collection]:
        """Get related collections."""
        response = await self._client.request("GET", f"/collections/{collection_id}/related")
        return [Collection.model_validate(item) for item in response.json()]
