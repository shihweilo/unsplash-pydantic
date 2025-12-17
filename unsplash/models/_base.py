from datetime import datetime
from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

T = TypeVar('T')

class UnsplashModel(BaseModel):
    """Base model for all Unsplash objects."""
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        # unknown fields are ignored to prevent breakage on API updates
        extra="ignore" 
    )

class Page(BaseModel, Generic[T]):
    """
    Paginated response wrapper.
    Manual pagination metadata provided by Unsplash headers.
    """
    results: List[T]
    total: int
    total_pages: int

    model_config = ConfigDict(populate_by_name=True)

class Links(BaseModel):
    """Common links structure found in many objects."""
    self: HttpUrl
    html: HttpUrl
    download: Optional[HttpUrl] = None
    download_location: Optional[HttpUrl] = None
