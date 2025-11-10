"""
Siray Python SDK

A Python client library for the Siray AI API.
"""

from .client import Siray
from .exceptions import (
    SirayError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    APIError,
)
from .models import (
    GenerationResponse,
    TaskStatus,
)

__version__ = "0.1.0"

__all__ = [
    "Siray",
    "SirayError",
    "AuthenticationError",
    "BadRequestError",
    "InternalServerError",
    "APIError",
    "GenerationResponse",
    "TaskStatus",
]
