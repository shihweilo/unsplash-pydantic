from ._client_base import HTTPClient, AsyncHTTPClient
from .resources import (
    PhotosResource,
    UsersResource,
    CollectionsResource,
    SearchResource
)

class UnsplashClient:
    """
    Synchronous Unsplash API Client.
    
    Args:
        access_key: Your Application ID (Access Key).
        base_url: Optional override for API base URL.
        timeout: Request timeout in seconds (default 30.0).
        max_retries: Number of retries for failed requests (default 3).
    """

    def __init__(
        self,
        access_key: str,
        base_url: str = "https://api.unsplash.com",
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self._http = HTTPClient(
            access_key=access_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries
        )
        self.photos = PhotosResource(self._http)
        self.users = UsersResource(self._http)
        self.collections = CollectionsResource(self._http)
        self.search = SearchResource(self._http)

class AsyncUnsplashClient:
    """
    Asynchronous Unsplash API Client.
    
    Args:
        access_key: Your Application ID (Access Key).
        base_url: Optional override for API base URL.
        timeout: Request timeout in seconds (default 30.0).
        max_retries: Number of retries for failed requests (default 3).
    """

    def __init__(
        self,
        access_key: str,
        base_url: str = "https://api.unsplash.com",
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self._http = AsyncHTTPClient(
            access_key=access_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries
        )
        self.photos = PhotosResource(self._http)
        self.users = UsersResource(self._http)
        self.collections = CollectionsResource(self._http)
        self.search = SearchResource(self._http)
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._http.aclose()
