"""Main Siray SDK client."""

from typing import Optional

from .base_client import BaseClient
from .resources.image import Image
from .resources.video import Video


class Siray:
    """
    Main client for interacting with Siray AI API.

    This client provides access to image and video generation capabilities
    through namespace attributes.

    Attributes:
        image: Image generation namespace
        video: Video generation namespace

    Example:
        >>> from siray import Siray
        >>> client = Siray(api_key="your-api-key")
        >>>
        >>> # Generate an image
        >>> result = client.image.generate_async(
        ...     model="black-forest-labs/flux-1.1-pro-ultra-i2i",
        ...     prompt="A beautiful sunset",
        ...     image="https://example.com/input.jpg"
        ... )
        >>>
        >>> # Generate a video
        >>> result = client.video.generate_async(
        ...     model="your-video-model",
        ...     prompt="A cat playing piano"
        ... )
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.siray.ai",
    ):
        """
        Initialize the Siray client.

        Args:
            api_key: API key for authentication. If not provided, will look for
                    SIRAY_API_KEY environment variable.
            base_url: Base URL for the API (default: https://api.siray.ai)

        Raises:
            ValueError: If no API key is provided or found in environment
        """
        if api_key is None:
            import os
            api_key = os.environ.get("SIRAY_API_KEY")

        if not api_key:
            raise ValueError(
                "API key must be provided either as argument or "
                "through SIRAY_API_KEY environment variable"
            )

        self._base_client = BaseClient(api_key=api_key, base_url=base_url)

        # Initialize namespaces
        self.image = Image(self._base_client)
        self.video = Video(self._base_client)

    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._base_client.api_key

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._base_client.base_url
