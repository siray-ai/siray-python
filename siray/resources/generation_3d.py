"""3D model generation resources for Siray SDK."""

import time
from typing import Any, Optional

from ..models import GenerationResponse, TaskStatus


class Generation3D:
    """3D model generation namespace.

    Supports both text-to-3D and image-to-3D generation models.

    Example:
        >>> client = Siray(api_key="your-api-key")
        >>>
        >>> # Text-to-3D
        >>> result = client.generation_3d.run(
        ...     model="tencent/hunyuan3d-v2.5-rapid-text-to-3d",
        ...     prompt="A cute cartoon cat",
        ... )
        >>>
        >>> # Image-to-3D
        >>> result = client.generation_3d.run(
        ...     model="tencent/hunyuan3d-v2.5-rapid-image-to-3d",
        ...     image="https://example.com/cat.png",
        ... )
    """

    def __init__(self, client):
        """
        Initialize the 3D Generation resource.

        Args:
            client: BaseClient instance for making API requests
        """
        self._client = client

    def generate_async(
        self,
        model: str,
        **kwargs: Any,
    ) -> GenerationResponse:
        """
        Generate a 3D model asynchronously using the specified model.

        For text-to-3D models, pass the ``prompt`` parameter.
        For image-to-3D models, pass the ``image`` parameter.

        Args:
            model: Model identifier (e.g., 'tencent/hunyuan3d-v2.5-rapid-text-to-3d')
            **kwargs: Model-specific parameters:
                - prompt (str): Text description for text-to-3D models
                - image (str): Input image URL or data URL for image-to-3D models
                - pbr_enable (bool): Enable PBR material output (default True)
                - texture_enable (bool): Enable texture generation (default True)

        Returns:
            GenerationResponse object containing task_id and other details

        Example:
            >>> client = Siray(api_key="your-api-key")
            >>> response = client.generation_3d.generate_async(
            ...     model="tencent/hunyuan3d-v2.5-rapid-text-to-3d",
            ...     prompt="A cute cartoon cat",
            ... )
            >>> print(response.task_id)
        """
        payload = {
            "model": model,
            **kwargs,
        }

        data = self._client.post("/v1/3d/generations", data=payload)
        return GenerationResponse(data)

    def query_task(self, task_id: str) -> TaskStatus:
        """
        Query the status and result of a 3D generation task.

        Args:
            task_id: Task ID returned from the 3D generation request

        Returns:
            TaskStatus object containing status, result, and other details

        Example:
            >>> client = Siray(api_key="your-api-key")
            >>> response = client.generation_3d.generate_async(
            ...     model="tencent/hunyuan3d-v2.5-rapid-text-to-3d",
            ...     prompt="A cute cartoon cat",
            ... )
            >>>
            >>> status = client.generation_3d.query_task(response.task_id)
            >>> if status.is_completed():
            ...     print(f"3D model URL: {status.result}")
            >>> elif status.is_failed():
            ...     print(f"Error: {status.fail_reason}")
        """
        data = self._client.get(f"/v1/3d/generations/{task_id}")
        return TaskStatus(data)

    def run(
        self,
        model: str,
        poll_interval: float = 2.0,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> TaskStatus:
        """
        Start an async 3D generation and poll until it finishes.

        Args:
            model: Model identifier
            poll_interval: Seconds to wait between status checks (default 2s)
            timeout: Maximum seconds to wait before raising TimeoutError (None disables)
            **kwargs: Model-specific parameters (prompt, image, pbr_enable, texture_enable, etc.)

        Returns:
            Final TaskStatus once the task completes or fails

        Raises:
            TimeoutError: If timeout is reached while the task is still processing
        """
        response = self.generate_async(model=model, **kwargs)
        poll_interval = max(poll_interval, 0.1)
        start_time = time.monotonic()

        while True:
            status = self.query_task(response.task_id)
            if not status.is_processing():
                return status

            if timeout is not None and (time.monotonic() - start_time) >= timeout:
                raise TimeoutError(
                    f"3D generation task {response.task_id} did not finish within {timeout} seconds"
                )

            time.sleep(poll_interval)
