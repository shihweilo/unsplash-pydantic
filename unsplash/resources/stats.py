from typing import TYPE_CHECKING

from ..models import MonthStats, TotalStats

if TYPE_CHECKING:
    from .._client_base import AsyncHTTPClient, HTTPClient


class StatsResource:
    """Handle platform-wide statistics endpoints."""

    def __init__(self, client: "HTTPClient"):
        self._client = client

    def total(self) -> TotalStats:
        """Totals for all of Unsplash."""
        response = self._client.request("GET", "/stats/total")
        return TotalStats.model_validate(response.json())

    def month(self) -> MonthStats:
        """Totals for the past 30 days."""
        response = self._client.request("GET", "/stats/month")
        return MonthStats.model_validate(response.json())


class AsyncStatsResource:
    """Async handle platform-wide statistics endpoints."""

    def __init__(self, client: "AsyncHTTPClient"):
        self._client = client

    async def total(self) -> TotalStats:
        """Totals for all of Unsplash."""
        response = await self._client.request("GET", "/stats/total")
        return TotalStats.model_validate(response.json())

    async def month(self) -> MonthStats:
        """Totals for the past 30 days."""
        response = await self._client.request("GET", "/stats/month")
        return MonthStats.model_validate(response.json())
