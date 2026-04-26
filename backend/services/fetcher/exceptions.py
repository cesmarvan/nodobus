"""Custom exceptions for the fetcher service."""


class FetcherException(Exception):
    """Base exception for fetcher service."""

    pass


class ExternalAPIError(FetcherException):
    """Raised when an external API call fails."""

    pass


class SyncError(FetcherException):
    """Raised when database synchronization fails."""

    pass


class ValidationError(FetcherException):
    """Raised when response validation fails."""

    pass
