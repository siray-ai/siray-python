"""Video generation resources for Siray SDK."""

from typing import Any

from ..models import GenerationResponse, TaskStatus


class Video:
    """Video generation namespace."""

    def __init__(self, client):
        """
        Initialize the Video resource.

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
        Generate a video asynchronously using the specified model.

        Args:
            model: Model identifier
            prompt: Text prompt for video generation
            **kwargs: Additional model-specific parameters (e.g., duration, fps, etc.)

        Returns:
            GenerationResponse object containing task_id and other details

        Example:
            >>> client = Siray(api_key="your-api-key")
            >>> response = client.video.generate_async(
            ...     model="your-video-model",
            ...     prompt="A cat playing piano"
            ... )
            >>> print(response.task_id)
        """
        payload = {
            "model": model,
            "prompt": prompt,
            **kwargs,
        }

        data = self._client.post("/v1/video/generations/async", data=payload)
        return GenerationResponse(data)

    def query_task(self, task_id: str) -> TaskStatus:
        """
        Query the status and result of a video generation task.

        Args:
            task_id: Task ID returned from the video generation request

        Returns:
            TaskStatus object containing status, result, and other details

        Example:
            >>> client = Siray(api_key="your-api-key")
            >>> # First, start an async generation
            >>> response = client.video.generate_async(
            ...     model="your-video-model",
            ...     prompt="A cat playing piano"
            ... )
            >>>
            >>> # Then query the task status
            >>> status = client.video.query_task(response.task_id)
            >>> if status.is_completed():
            ...     print(f"Video URL: {status.result}")
            >>> elif status.is_failed():
            ...     print(f"Error: {status.fail_reason}")
        """
        data = self._client.get(f"/v1/video/generations/async/{task_id}")
        return TaskStatus(data)
