import builtins
from typing import TYPE_CHECKING, Any, Optional

from ..models import Photo, Topic

if TYPE_CHECKING:
    from .._client_base import AsyncHTTPClient, HTTPClient


def _list_params(
    ids: Optional[list[str]],
    page: int,
    per_page: int,
    order_by: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "page": page,
        "per_page": per_page,
        "order_by": order_by,
    }
    if ids:
        params["ids"] = ",".join(ids)
    return params


def _photos_params(
    page: int,
    per_page: int,
    orientation: Optional[str],
    order_by: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "page": page,
        "per_page": per_page,
        "order_by": order_by,
    }
    if orientation:
        params["orientation"] = orientation
    return params


class TopicsResource:
    """Handle topic-related endpoints."""

    def __init__(self, client: "HTTPClient"):
        self._client = client

    def list(
        self,
        ids: Optional[list[str]] = None,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "position",
    ) -> list[Topic]:
        """
        List topics.

        Args:
            ids: Limit to these topic ids or slugs.
            order_by: One of ``featured``, ``latest``, ``oldest``, ``position``.
        """
        response = self._client.request(
            "GET", "/topics", params=_list_params(ids, page, per_page, order_by)
        )
        return [Topic.model_validate(item) for item in response.json()]

    def get(self, id_or_slug: str) -> Topic:
        """Retrieve a single topic by id or slug."""
        response = self._client.request("GET", f"/topics/{id_or_slug}")
        return Topic.model_validate(response.json())

    def photos(
        self,
        id_or_slug: str,
        page: int = 1,
        per_page: int = 10,
        orientation: Optional[str] = None,
        order_by: str = "latest",
    ) -> builtins.list[Photo]:
        """
        Get a topic's photos.

        Args:
            order_by: One of ``latest``, ``oldest``, ``popular``.
        """
        response = self._client.request(
            "GET",
            f"/topics/{id_or_slug}/photos",
            params=_photos_params(page, per_page, orientation, order_by),
        )
        return [Photo.model_validate(item) for item in response.json()]


class AsyncTopicsResource:
    """Async handle topic-related endpoints."""

    def __init__(self, client: "AsyncHTTPClient"):
        self._client = client

    async def list(
        self,
        ids: Optional[list[str]] = None,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "position",
    ) -> list[Topic]:
        """
        List topics.

        Args:
            ids: Limit to these topic ids or slugs.
            order_by: One of ``featured``, ``latest``, ``oldest``, ``position``.
        """
        response = await self._client.request(
            "GET", "/topics", params=_list_params(ids, page, per_page, order_by)
        )
        return [Topic.model_validate(item) for item in response.json()]

    async def get(self, id_or_slug: str) -> Topic:
        """Retrieve a single topic by id or slug."""
        response = await self._client.request("GET", f"/topics/{id_or_slug}")
        return Topic.model_validate(response.json())

    async def photos(
        self,
        id_or_slug: str,
        page: int = 1,
        per_page: int = 10,
        orientation: Optional[str] = None,
        order_by: str = "latest",
    ) -> builtins.list[Photo]:
        """
        Get a topic's photos.

        Args:
            order_by: One of ``latest``, ``oldest``, ``popular``.
        """
        response = await self._client.request(
            "GET",
            f"/topics/{id_or_slug}/photos",
            params=_photos_params(page, per_page, orientation, order_by),
        )
        return [Photo.model_validate(item) for item in response.json()]
