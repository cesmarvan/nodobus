"""HTTP client for accessing TUSSAM real-time API."""

import logging

import httpx

logger = logging.getLogger(__name__)


class TussamAPIClient:
    """HTTP client for TUSSAM real-time buses API."""

    BASE_URL = "https://reddelineas.tussam.es/API/infotus-ui/buses"

    def __init__(self, timeout: int = 10):
        """Initialize TUSSAM API client.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout

    async def get_buses_by_line(self, line_label: str) -> dict:
        """Get real-time buses for a specific line.

        Args:
            line_label: Line label/number (e.g., "25", "C3")

        Returns:
            JSON response with bus data

        Raises:
            httpx.HTTPError: If request fails
        """
        url = f"{self.BASE_URL}/{line_label}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                logger.debug(f"TUSSAM API response status: {response.status_code}")
                logger.debug(f"TUSSAM API response headers: {response.headers}")
                
                response.raise_for_status()
                
                # Try to parse as JSON
                try:
                    data = response.json()
                    logger.debug(f"Successfully parsed JSON from TUSSAM API")
                    return data
                except ValueError as json_error:
                    # If JSON parse fails, log the response text
                    response_text = response.text[:500]  # First 500 chars
                    logger.error(f"Failed to parse JSON response. Response text: {response_text}")
                    raise ValueError(f"TUSSAM API returned non-JSON response: {response_text}") from json_error
                    
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching buses for line {line_label}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching buses for line {line_label}: {e}")
            raise
