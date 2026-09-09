from ._client_base import AsyncHTTPClient, HTTPClient
from .resources import (
    AsyncCollectionsResource,
    AsyncPhotosResource,
    AsyncSearchResource,
    AsyncTopicsResource,
    AsyncUsersResource,
    CollectionsResource,
    PhotosResource,
    SearchResource,
    TopicsResource,
    UsersResource,
)


class UnsplashClient:
    """
    Synchronous Unsplash API Client.

    Args:
        access_key: Your Application ID (Access Key).
        base_url: Optional override for API base URL.
        timeout: Request timeout in seconds (default 30.0).
        max_retries: Retries for transport errors and 5xx responses
            (default 3). A 429 is only retried when the response carries a
            short Retry-After; Unsplash's quota is hourly, so retrying it
            otherwise just delays the error.
    """

    def __init__(
        self,
        access_key: str,
        base_url: str = "https://api.unsplash.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self._http = HTTPClient(
            access_key=access_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.photos = PhotosResource(self._http)
        self.users = UsersResource(self._http)
        self.collections = CollectionsResource(self._http)
        self.search = SearchResource(self._http)
        self.topics = TopicsResource(self._http)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> "UnsplashClient":
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()


class AsyncUnsplashClient:
    """
    Asynchronous Unsplash API Client.

    Args:
        access_key: Your Application ID (Access Key).
        base_url: Optional override for API base URL.
        timeout: Request timeout in seconds (default 30.0).
        max_retries: Retries for transport errors and 5xx responses
            (default 3). A 429 is only retried when the response carries a
            short Retry-After; Unsplash's quota is hourly, so retrying it
            otherwise just delays the error.
    """

    def __init__(
        self,
        access_key: str,
        base_url: str = "https://api.unsplash.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self._http = AsyncHTTPClient(
            access_key=access_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.photos = AsyncPhotosResource(self._http)
        self.users = AsyncUsersResource(self._http)
        self.collections = AsyncCollectionsResource(self._http)
        self.search = AsyncSearchResource(self._http)
        self.topics = AsyncTopicsResource(self._http)

    async def aclose(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncUnsplashClient":
        return self

    async def __aexit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        await self.aclose()
