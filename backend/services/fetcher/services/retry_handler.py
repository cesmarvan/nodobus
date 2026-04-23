"""Retry handler with exponential backoff for API requests."""

import asyncio
import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast

import httpx

from services.fetcher.exceptions import ExternalAPIError

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class RetryConfig:
    """Configuration for retry logic."""

    def __init__(
        self,
        base_delay: float = 1.0,
        max_retries: int = 3,
        max_delay: float = 60.0,
        backoff_multiplier: float = 2.0,
    ):
        """Initialize retry configuration.

        Args:
            base_delay: Initial delay in seconds between retries
            max_retries: Maximum number of retry attempts
            max_delay: Maximum delay between retries (cap for exponential backoff)
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.base_delay = base_delay
        self.max_retries = max_retries
        self.max_delay = max_delay
        self.backoff_multiplier = backoff_multiplier

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number.

        Args:
            attempt: Attempt number (0-indexed)

        Returns:
            Delay in seconds
        """
        delay = self.base_delay * (self.backoff_multiplier**attempt)
        return min(delay, self.max_delay)


def retry_with_backoff(
    config: RetryConfig | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying async functions with exponential backoff.

    Args:
        config: RetryConfig instance for retry behavior

    Returns:
        Decorated function
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (
                    httpx.HTTPError,
                    httpx.RequestError,
                    httpx.TimeoutException,
                    asyncio.TimeoutError,
                ) as e:
                    last_exception = e

                    # Don't retry on 4xx errors (client errors)
                    if isinstance(e, httpx.HTTPStatusError) and 400 <= e.response.status_code < 500:
                        logger.warning(
                            f"Client error (4xx) in {func.__name__}, not retrying: {e}",
                        )
                        raise ExternalAPIError(f"Client error: {e}") from e

                    if attempt < config.max_retries:
                        delay = config.get_delay(attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}, "
                            f"retrying in {delay}s: {e}",
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {config.max_retries + 1} attempts failed for {func.__name__}: {e}",
                        )

            raise ExternalAPIError(
                f"Failed after {config.max_retries + 1} attempts",
            ) from last_exception

        return cast(F, wrapper)

    return decorator
