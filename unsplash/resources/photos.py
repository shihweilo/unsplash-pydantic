from typing import List, Optional, Union, TYPE_CHECKING
from ..models import Photo

if TYPE_CHECKING:
    from .._client_base import HTTPClient

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
        params = {}
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
        return response.json()["url"]

    def download(self, photo_id: str, track: bool = True) -> str:
        """
        Get the download URL for a photo.
        
        Args:
            photo_id: The ID of the photo.
            track: Whether to report the download to Unsplash (required by API guidelines).
                   Defaults to True.
        
        Returns:
            The direct URL to the photo.
        """
        if track:
            return self.track_download(photo_id)
        
        # If not tracking, we must look up the photo URL manually (or via get)
        # But per specific request in rules.md "Return image URLs directly... No local caching"
        # and "return photo.urls.full" in the example.
        photo = self.get(photo_id)
        return str(photo.urls.full)
