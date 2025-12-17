from typing import List, Optional, Any

class UnsplashError(Exception):
    """Base exception for all Unsplash errors."""
    
    def __init__(
        self,
        message: str,
        http_status: Optional[int] = None,
        http_body: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.http_status = http_status
        self.http_body = http_body

class AuthenticationError(UnsplashError):
    """Invalid access key (401)."""
    pass

class RateLimitError(UnsplashError):
    """Rate limit exceeded (429)."""
    
    def __init__(
        self,
        message: str,
        limit: Optional[int] = None,
        remaining: Optional[int] = None,
        **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.limit = limit
        self.remaining = remaining

class NotFoundError(UnsplashError):
    """Resource not found (404)."""
    pass

class ValidationError(UnsplashError):
    """Invalid request parameters (422)."""
    
    def __init__(self, message: str, errors: List[str], **kwargs: Any):
        super().__init__(message, **kwargs)
        self.errors = errors
