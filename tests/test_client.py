"""Tests for Siray client."""

import os
import pytest
from siray import Siray
from siray.exceptions import (
    SirayError,
    AuthenticationError,
    BadRequestError,
)


class TestSirayClient:
    """Test Siray client initialization and basic functionality."""

    def test_client_initialization_with_api_key(self):
        """Test client initialization with API key parameter."""
        client = Siray(api_key="test-api-key")
        assert client.api_key == "test-api-key"
        assert client.base_url == "https://api.siray.ai"

    def test_client_initialization_with_custom_base_url(self):
        """Test client initialization with custom base URL."""
        client = Siray(api_key="test-api-key", base_url="https://custom.api.url")
        assert client.base_url == "https://custom.api.url"

    def test_client_initialization_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        # Clear environment variable if it exists
        old_key = os.environ.get("SIRAY_API_KEY")
        if old_key:
            del os.environ["SIRAY_API_KEY"]

        with pytest.raises(ValueError, match="API key must be provided"):
            Siray()

        # Restore environment variable
        if old_key:
            os.environ["SIRAY_API_KEY"] = old_key

    def test_client_initialization_from_environment(self):
        """Test client initialization from environment variable."""
        os.environ["SIRAY_API_KEY"] = "env-test-key"

        client = Siray()
        assert client.api_key == "env-test-key"

        # Cleanup
        del os.environ["SIRAY_API_KEY"]

    def test_client_has_namespaces(self):
        """Test that client has image and video namespaces."""
        client = Siray(api_key="test-api-key")
        assert hasattr(client, "image")
        assert hasattr(client, "video")


class TestImageNamespace:
    """Test Image namespace methods."""

    def test_image_has_required_methods(self):
        """Test that image namespace has required methods."""
        client = Siray(api_key="test-api-key")
        assert hasattr(client.image, "generate_async")
        assert hasattr(client.image, "query_task")
        assert hasattr(client.image, "run")


class TestVideoNamespace:
    """Test Video namespace methods."""

    def test_video_has_required_methods(self):
        """Test that video namespace has required methods."""
        client = Siray(api_key="test-api-key")
        assert hasattr(client.video, "generate_async")
        assert hasattr(client.video, "query_task")
        assert hasattr(client.video, "run")
