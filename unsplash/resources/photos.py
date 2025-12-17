from typing import List, Optional, Union, TYPE_CHECKING, Dict, Any
from ..models import Photo

if TYPE_CHECKING:
    from .._client_base import HTTPClient, AsyncHTTPClient

class PhotosResource:
    """Handle all photo-related endpoints."""
    
    def __init__(self, client: "HTTPClient"):
        self._client = client
    
    def get(self, photo_id: str) -> Photo:
        """Retrieve a single photo."""
        response = self._client.request("GET", f"/photos/{photo_id}")
        return Photo.model_validate(response.json())
    
    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "latest"
    ) -> List[Photo]:
        """List photos from editorial feed."""
        response = self._client.request(
            "GET",
            "/photos",
            params={
                "page": page,
                "per_page": per_page,
                "order_by": order_by
            }
        )
        return [Photo.model_validate(item) for item in response.json()]
    
    def random(
        self,
        query: Optional[str] = None,
        orientation: Optional[str] = None,
        collections: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        username: Optional[str] = None,
        count: Optional[int] = None
    ) -> Union[Photo, List[Photo]]:
        """Get random photo(s)."""
        params: Dict[str, Any] = {}
        if query: params["query"] = query
        if orientation: params["orientation"] = orientation
        if collections: params["collections"] = ",".join(collections)
        if topics: params["topics"] = ",".join(topics)
        if username: params["username"] = username
        if count: params["count"] = count
        
        response = self._client.request("GET", "/photos/random", params=params)
        data = response.json()
        
        if isinstance(data, list):
            return [Photo.model_validate(item) for item in data]
        return Photo.model_validate(data)
    
    def track_download(self, photo_id: str) -> str:
        """Track photo download (required by API guidelines)."""
        response = self._client.request("GET", f"/photos/{photo_id}/download")
        return str(response.json()["url"])

    def download(self, photo_id: str, track: bool = True) -> str:
        """
        Get the download URL for a photo.
        """
        if track:
            return self.track_download(photo_id)
        
        photo = self.get(photo_id)
        return str(photo.urls.full)


class AsyncPhotosResource:
    """Async handle all photo-related endpoints."""
    
    def __init__(self, client: "AsyncHTTPClient"):
        self._client = client
    
    async def get(self, photo_id: str) -> Photo:
        """Retrieve a single photo."""
        response = await self._client.request("GET", f"/photos/{photo_id}")
        return Photo.model_validate(response.json())
    
    async def list(
        self,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "latest"
    ) -> List[Photo]:
        """List photos from editorial feed."""
        response = await self._client.request(
            "GET",
            "/photos",
            params={
                "page": page,
                "per_page": per_page,
                "order_by": order_by
            }
        )
        return [Photo.model_validate(item) for item in response.json()]
    
    async def random(
        self,
        query: Optional[str] = None,
        orientation: Optional[str] = None,
        collections: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        username: Optional[str] = None,
        count: Optional[int] = None
    ) -> Union[Photo, List[Photo]]:
        """Get random photo(s)."""
        params: Dict[str, Any] = {}
        if query: params["query"] = query
        if orientation: params["orientation"] = orientation
        if collections: params["collections"] = ",".join(collections)
        if topics: params["topics"] = ",".join(topics)
        if username: params["username"] = username
        if count: params["count"] = count
        
        response = await self._client.request("GET", "/photos/random", params=params)
        data = response.json()
        
        if isinstance(data, list):
            return [Photo.model_validate(item) for item in data]
        return Photo.model_validate(data)
    
    async def track_download(self, photo_id: str) -> str:
        """Track photo download (required by API guidelines)."""
        response = await self._client.request("GET", f"/photos/{photo_id}/download")
        return str(response.json()["url"])

    async def download(self, photo_id: str, track: bool = True) -> str:
        """
        Get the download URL for a photo.
        """
        if track:
            return await self.track_download(photo_id)
        
        photo = await self.get(photo_id)
        return str(photo.urls.full)
