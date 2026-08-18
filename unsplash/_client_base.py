import asyncio
import email.utils
import time
from typing import Any, Optional

import httpx

from .errors import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    UnsplashError,
    ValidationError,
)

#: Server-side failures that are worth retrying. 429 is handled separately:
#: Unsplash rate limits are hourly, so a blind retry just burns attempts.
RETRY_STATUS_CODES = frozenset({500, 502, 503, 504})

#: Backoff is deterministic (no jitter) so behavior stays predictable and testable.
BACKOFF_FACTOR = 0.5
MAX_BACKOFF = 30.0

#: A 429 is only retried when the server tells us to wait, and only if that
#: wait is short. Unsplash's hourly quota otherwise makes retrying pointless.
MAX_RETRY_AFTER = 60.0


def _parse_retry_after(value: Optional[str]) -> Optional[float]:
    """Parse a Retry-After header (delay-seconds or HTTP-date) into seconds."""
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        retry_at = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if retry_at is None:
        return None
    delta = retry_at.timestamp() - time.time()
    return max(0.0, delta)


def _backoff_delay(attempt: int) -> float:
    """Exponential backoff for the given zero-based attempt number."""
    return min(BACKOFF_FACTOR * float(2**attempt), MAX_BACKOFF)


def _retry_delay(response: httpx.Response, attempt: int) -> Optional[float]:
    """
    Seconds to wait before retrying this response, or None to not retry.

    Assumes the caller has already confirmed retries remain.
    """
    retry_after = _parse_retry_after(response.headers.get("Retry-After"))

    if response.status_code == 429:
        if retry_after is not None and retry_after <= MAX_RETRY_AFTER:
            return retry_after
        return None

    if response.status_code in RETRY_STATUS_CODES:
        if retry_after is not None and retry_after <= MAX_RETRY_AFTER:
            return retry_after
        return _backoff_delay(attempt)

    return None


class HTTPClient:
    """Sync/async HTTP client for API requests."""

    def __init__(
        self,
        access_key: str,
        base_url: str = "https://api.unsplash.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.access_key = access_key
        self.base_url = base_url
        self.max_retries = max_retries
        self._client = httpx.Client(timeout=timeout)

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Client-ID {self.access_key}"
        headers["Accept-Version"] = "v1"
        url = f"{self.base_url}{path}"

        for attempt in range(self.max_retries + 1):
            retries_left = attempt < self.max_retries
            try:
                response = self._client.request(method, url, headers=headers, **kwargs)
            except httpx.TransportError:
                # Connection reset, DNS failure, timeout: retry if budget allows.
                if not retries_left:
                    raise
                time.sleep(_backoff_delay(attempt))
                continue

            if not retries_left:
                break
            delay = _retry_delay(response, attempt)
            if delay is None:
                break
            response.close()
            time.sleep(delay)

        self._check_error(response)
        return response

    def close(self) -> None:
        """Close the underlying connection pool."""
        self._client.close()

    def __enter__(self) -> "HTTPClient":
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

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
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.access_key = access_key
        self.base_url = base_url
        self.max_retries = max_retries
        self._client = httpx.AsyncClient(timeout=timeout)

    async def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Client-ID {self.access_key}"
        headers["Accept-Version"] = "v1"
        url = f"{self.base_url}{path}"

        for attempt in range(self.max_retries + 1):
            retries_left = attempt < self.max_retries
            try:
                response = await self._client.request(
                    method, url, headers=headers, **kwargs
                )
            except httpx.TransportError:
                # Connection reset, DNS failure, timeout: retry if budget allows.
                if not retries_left:
                    raise
                await asyncio.sleep(_backoff_delay(attempt))
                continue

            if not retries_left:
                break
            delay = _retry_delay(response, attempt)
            if delay is None:
                break
            await response.aclose()
            await asyncio.sleep(delay)

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
        """Close the underlying connection pool."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncHTTPClient":
        return self

    async def __aexit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        await self.aclose()
