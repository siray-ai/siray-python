"""Base HTTP client for Siray SDK."""

import json
from typing import Any, Dict, Optional
from urllib.parse import urljoin

try:
    import httpx
except ImportError:
    import requests as httpx  # Fallback to requests if httpx not available

from .exceptions import (
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    APIError,
)


class BaseClient:
    """Base HTTP client for making API requests."""

    def __init__(self, api_key: str, base_url: str = "https://api.siray.ai", timeout: int = 120):
        """
        Initialize the base client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API (default: https://api.siray.ai)
            timeout: Request timeout in seconds (default: 120)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _handle_error_response(self, status_code: int, response_data: Dict[str, Any]):
        """Handle error responses from the API."""
        error_info = response_data.get("error", {})
        message = error_info.get("message", "Unknown error")

        if status_code == 401:
            raise AuthenticationError(message, status_code=status_code)
        elif status_code == 400:
            code = error_info.get("code")
            error_type = error_info.get("type")
            raise BadRequestError(message, code=code, error_type=error_type, status_code=status_code)
        elif status_code == 500:
            raise InternalServerError(message, status_code=status_code)
        else:
            raise APIError(message, status_code=status_code)

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            AuthenticationError: If authentication fails
            BadRequestError: If the request is invalid
            InternalServerError: If the server encounters an error
            APIError: For other API errors
        """
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        headers = self._get_headers()

        try:
            # Try using httpx first
            if hasattr(httpx, 'Client'):
                with httpx.Client() as client:
                    response = client.request(
                        method=method,
                        url=url,
                        json=data,
                        params=params,
                        headers=headers,
                        timeout=self.timeout,
                    )
            else:
                # Fallback to requests
                response = httpx.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )

            # Parse response
            try:
                response_data = response.json()
            except (json.JSONDecodeError, ValueError):
                response_data = {}

            # Check for errors
            if response.status_code >= 400:
                self._handle_error_response(response.status_code, response_data)

            return response_data

        except (AuthenticationError, BadRequestError, InternalServerError, APIError):
            raise
        except Exception as e:
            raise APIError(f"Request failed: {str(e)}")

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return self._request("POST", endpoint, data=data)

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a GET request."""
        return self._request("GET", endpoint, params=params)
