"""Custom exceptions for Siray SDK."""


class SirayError(Exception):
    """Base exception for all Siray SDK errors."""

    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(SirayError):
    """Raised when authentication fails (401)."""
    pass


class BadRequestError(SirayError):
    """Raised when the request is invalid (400)."""

    def __init__(self, message: str, code: str = None, error_type: str = None, status_code: int = 400):
        super().__init__(message, status_code)
        self.code = code
        self.error_type = error_type


class InternalServerError(SirayError):
    """Raised when the server encounters an error (500)."""
    pass


class APIError(SirayError):
    """Raised for general API errors."""
    pass
