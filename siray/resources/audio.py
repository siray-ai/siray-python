"""Audio generation resources for Siray SDK."""

import time
from typing import Any, Dict, Optional

from ..models import GenerationResponse, TaskStatus


class Audio:
    """Audio/music generation namespace."""

    def __init__(self, client):
        self._client = client

    def generate_async(
        self,
        model: str,
        prompt: str,
        **kwargs: Any,
    ) -> GenerationResponse:
        """Generate audio asynchronously.

        Args:
            model: Model identifier, e.g. ``minimax/music-3.0``.
            prompt: Music description.
            **kwargs: Model-specific parameters such as ``lyrics``,
                ``lyrics_optimizer``, ``is_instrumental``, ``bitrate`` and
                ``sample_rate``.

        Example:
            >>> client.audio.generate_async(
            ...     model="minimax/music-3.0",
            ...     prompt="Cinematic pop song",
            ...     lyrics="[Verse]\nI left the light on",
            ...     is_instrumental=False,
            ... )
        """
        payload: Dict[str, Any] = {"model": model, "prompt": prompt}
        payload.update(kwargs)

        data = self._client.post("/v1/audio/generations", data=payload)
        return GenerationResponse(data)

    def query_task(self, task_id: str) -> TaskStatus:
        """Query an audio generation task."""
        data = self._client.get(f"/v1/audio/generations/{task_id}")
        return TaskStatus(data)

    def run(
        self,
        model: str,
        prompt: str,
        poll_interval: float = 2.0,
        timeout: Optional[float] = 10 * 60,
        **kwargs: Any,
    ) -> TaskStatus:
        """Start an async audio generation and poll until it finishes.

        The default timeout is 10 minutes because music generation can be slow.
        """
        response = self.generate_async(model=model, prompt=prompt, **kwargs)
        poll_interval = max(poll_interval, 0.1)
        start_time = time.monotonic()

        while True:
            status = self.query_task(response.task_id)
            if not status.is_processing():
                return status

            if timeout is not None and (time.monotonic() - start_time) >= timeout:
                raise TimeoutError(
                    f"Audio task {response.task_id} did not finish within {timeout} seconds"
                )

            time.sleep(poll_interval)
