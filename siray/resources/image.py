"""Image generation resources for Siray SDK."""

from typing import Any

from ..models import GenerationResponse, TaskStatus


class Image:
    """Image generation namespace."""

    def __init__(self, client):
        """
        Initialize the Image resource.

        Args:
            client: BaseClient instance for making API requests
        """
        self._client = client

    def generate_async(
        self,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> GenerationResponse:
        """
        Generate an image asynchronously using the specified model.

        Args:
            model: Model identifier (e.g., 'black-forest-labs/flux-1.1-pro-ultra-i2i')
            prompt: Text prompt for image generation
            **kwargs: Additional model-specific parameters

        Returns:
            GenerationResponse object containing task_id and other details

        Example:
            >>> client = Siray(api_key="your-api-key")
            >>> response = client.image.generate_async(
            ...     model="black-forest-labs/flux-1.1-pro-ultra-i2i",
            ...     prompt="A beautiful sunset over mountains",
            ...     image="https://example.com/input.jpg"
            ... )
            >>> print(response.task_id)
        """
        payload = {
            "model": model,
            "prompt": prompt,
            **kwargs,
        }

        data = self._client.post("/v1/images/generations/async", data=payload)
        return GenerationResponse(data)

    def query_task(self, task_id: str) -> TaskStatus:
        """
        Query the status and result of an image generation task.

        Args:
            task_id: Task ID returned from the image generation request

        Returns:
            TaskStatus object containing status, result, and other details

        Example:
            >>> client = Siray(api_key="your-api-key")
            >>> # First, start an async generation
            >>> response = client.image.generate_async(
            ...     model="black-forest-labs/flux-kontext-i2i-max",
            ...     prompt="A beautiful sunset over mountains",
            ...     image="https://example.com/input.jpg"
            ... )
            >>>
            >>> # Then query the task status
            >>> status = client.image.query_task(response.task_id)
            >>> if status.is_completed():
            ...     print(f"Image URL: {status.result}")
            >>> elif status.is_failed():
            ...     print(f"Error: {status.error}")
        """
        data = self._client.get(f"/v1/images/generations/async/{task_id}")
        return TaskStatus(data)
