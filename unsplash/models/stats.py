import datetime
from typing import Optional

from ._base import UnsplashModel


class HistoricalValue(UnsplashModel):
    """A single point in a historical statistics series."""

    date: Optional[datetime.date] = None
    value: Optional[int] = None


class HistoricalData(UnsplashModel):
    """The historical breakdown attached to a statistic."""

    change: Optional[int] = None
    average: Optional[int] = None
    resolution: Optional[str] = None
    quantity: Optional[int] = None
    values: list[HistoricalValue] = []


class Statistic(UnsplashModel):
    """A single counter with its historical series."""

    total: Optional[int] = None
    historical: Optional[HistoricalData] = None


class PhotoStatistics(UnsplashModel):
    """Statistics for a single photo."""

    id: Optional[str] = None
    downloads: Optional[Statistic] = None
    views: Optional[Statistic] = None
    likes: Optional[Statistic] = None


class UserStatistics(UnsplashModel):
    """Statistics for a single user."""

    username: Optional[str] = None
    downloads: Optional[Statistic] = None
    views: Optional[Statistic] = None
    likes: Optional[Statistic] = None


class TotalStats(UnsplashModel):
    """Platform-wide totals from ``GET /stats/total``."""

    total_photos: Optional[int] = None
    photos: Optional[int] = None
    downloads: Optional[int] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    photographers: Optional[int] = None
    pixels: Optional[int] = None
    downloads_per_second: Optional[int] = None
    views_per_second: Optional[int] = None
    developers: Optional[int] = None
    applications: Optional[int] = None
    requests: Optional[int] = None


class MonthStats(UnsplashModel):
    """Trailing-month totals from ``GET /stats/month``."""

    downloads: Optional[int] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    new_photos: Optional[int] = None
    new_photographers: Optional[int] = None
    new_pixels: Optional[int] = None
    new_developers: Optional[int] = None
    new_applications: Optional[int] = None
    new_requests: Optional[int] = None
