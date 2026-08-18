from typing import Any

import httpx

from .errors import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    UnsplashError,
    ValidationError,
)


class HTTPClient:
    """Sync/async HTTP client for API requests."""

    def __init__(
        self,
        access_key: str,
        base_url: str = "https://api.unsplash.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.access_key = access_key
        self.base_url = base_url
        self.max_retries = max_retries
        self._client = httpx.Client(timeout=timeout)

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Client-ID {self.access_key}"
        headers["Accept-Version"] = "v1"

        response = self._client.request(
            method, f"{self.base_url}{path}", headers=headers, **kwargs
        )
        self._check_error(response)
        return response

    def _check_error(self, response: httpx.Response) -> None:
        """Convert HTTP errors to domain exceptions."""
        if response.is_success:
            return

        status = response.status_code
        body = response.text

        try:
            data = response.json()
            errors = data.get("errors", [])
            message = ", ".join(errors) if errors else body
        except Exception:
            message = body
            data = {}

        if status == 401:
            raise AuthenticationError(message, status, body)
        elif status == 404:
            raise NotFoundError(message, status, body)
        elif status == 422:
            errors = data.get("errors", [])
            raise ValidationError(message, errors, http_status=status, http_body=body)
        elif status == 429:
            limit = int(response.headers.get("X-Ratelimit-Limit", 0))
            remaining = int(response.headers.get("X-Ratelimit-Remaining", 0))
            raise RateLimitError(
                message, limit, remaining, http_status=status, http_body=body
            )
        else:
            raise UnsplashError(message, status, body)


class AsyncHTTPClient:
    """Async variant of HTTPClient."""

    def __init__(
        self,
        access_key: str,
        base_url: str = "https://api.unsplash.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.access_key = access_key
        self.base_url = base_url
        self.max_retries = max_retries
        self._client = httpx.AsyncClient(timeout=timeout)

    async def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Client-ID {self.access_key}"
        headers["Accept-Version"] = "v1"

        response = await self._client.request(
            method, f"{self.base_url}{path}", headers=headers, **kwargs
        )
        self._check_error(response)
        return response

    def _check_error(self, response: httpx.Response) -> None:
        """Reuse error checking logic (identical behavior)."""
        # Duplicated from HTTPClient rather than shared via a mixin; kept simple
        # for now. See the roadmap note about hoisting this into a helper.
        if response.is_success:
            return

        status = response.status_code
        body = response.text

        try:
            data = response.json()
            errors = data.get("errors", [])
            message = ", ".join(errors) if errors else body
        except Exception:
            message = body
            data = {}

        if status == 401:
            raise AuthenticationError(message, status, body)
        elif status == 404:
            raise NotFoundError(message, status, body)
        elif status == 422:
            errors = data.get("errors", [])
            raise ValidationError(message, errors, http_status=status, http_body=body)
        elif status == 429:
            limit = int(response.headers.get("X-Ratelimit-Limit", 0))
            remaining = int(response.headers.get("X-Ratelimit-Remaining", 0))
            raise RateLimitError(
                message, limit, remaining, http_status=status, http_body=body
            )
        else:
            raise UnsplashError(message, status, body)

    async def aclose(self) -> None:
        await self._client.aclose()
