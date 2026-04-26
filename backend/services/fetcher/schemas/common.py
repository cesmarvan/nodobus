"""Common schemas for fetcher responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Error detail in fetch operation."""

    code: str
    message: str
    details: dict[str, Any] | None = None


class FetchResultResponse(BaseModel):
    """Response for fetch operations."""

    status: str  # "success", "partial", "failed"
    count_created: int
    count_updated: int
    count_failed: int
    errors: list[ErrorDetail] = []
    timestamp: datetime
    duration_seconds: float

    class Config:
        from_attributes = True
