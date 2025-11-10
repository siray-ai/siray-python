"""Tests for Siray exceptions."""

import pytest
from siray.exceptions import (
    SirayError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    APIError,
)


class TestExceptions:
    """Test exception classes."""

    def test_siray_error(self):
        """Test SirayError base exception."""
        error = SirayError("Test error", status_code=400)
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.status_code == 400

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Invalid API key", status_code=401)
        assert error.message == "Invalid API key"
        assert error.status_code == 401
        assert isinstance(error, SirayError)

    def test_bad_request_error(self):
        """Test BadRequestError."""
        error = BadRequestError(
            "Invalid parameter",
            code="invalid_param",
            error_type="validation_error",
            status_code=400
        )
        assert error.message == "Invalid parameter"
        assert error.code == "invalid_param"
        assert error.error_type == "validation_error"
        assert error.status_code == 400
        assert isinstance(error, SirayError)

    def test_internal_server_error(self):
        """Test InternalServerError."""
        error = InternalServerError("Server error", status_code=500)
        assert error.message == "Server error"
        assert error.status_code == 500
        assert isinstance(error, SirayError)

    def test_api_error(self):
        """Test APIError."""
        error = APIError("API error", status_code=502)
        assert error.message == "API error"
        assert error.status_code == 502
        assert isinstance(error, SirayError)
