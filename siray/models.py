"""Response models for Siray SDK."""

from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field


@dataclass
class GenerationResponse:
    """Response from an async generation request.

    Attributes:
        task_id: Unique identifier for the generation task
        raw_response: Raw response data from the API
    """
    task_id: str
    raw_response: Dict[str, Any] = field(default_factory=dict, repr=False)

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize from API response data.

        Args:
            data: Raw response dictionary from the API
        """
        self.task_id = data.get("task_id", data.get("id", ""))
        self.raw_response = data

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.raw_response


@dataclass
class TaskStatus:
    """Status of a generation task.

    Attributes:
        code: Response code (e.g., 'success')
        message: Response message
        task_id: Unique identifier for the task
        action: Action type (e.g., 'imageGenerate')
        status: Current status of the task (e.g., 'SUCCESS', 'PENDING', 'FAILED')
        outputs: List of output URLs
        fail_reason: Failure reason if task failed
        progress: Progress string (e.g., '100%')
        submit_time: Unix timestamp when task was submitted
        start_time: Unix timestamp when task started
        finish_time: Unix timestamp when task finished
        raw_response: Raw response data from the API
    """
    code: str
    message: str
    task_id: str
    action: str
    status: str
    outputs: List[str] = field(default_factory=list)
    fail_reason: Optional[str] = None
    progress: Optional[str] = None
    submit_time: Optional[int] = None
    start_time: Optional[int] = None
    finish_time: Optional[int] = None
    raw_response: Dict[str, Any] = field(default_factory=dict, repr=False)

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize from API response data.

        Args:
            data: Raw response dictionary from the API
                Expected format:
                {
                    "code": "success",
                    "message": "",
                    "data": {
                        "task_id": "...",
                        "action": "imageGenerate",
                        "status": "SUCCESS",
                        "outputs": ["url1", "url2"],
                        "fail_reason": "...",
                        "progress": "100%",
                        "submit_time": 1762512511,
                        "start_time": 1762512515,
                        "finish_time": 1762512530
                    }
                }
        """
        self.raw_response = data

        # Extract top-level fields
        self.code = data.get("code", "unknown")
        self.message = data.get("message", "")

        # Extract task data from nested 'data' field
        task_data = data.get("data", {})
        self.task_id = task_data.get("task_id", "")
        self.action = task_data.get("action", "")
        self.status = task_data.get("status", "UNKNOWN")
        self.outputs = task_data.get("outputs", [])
        self.fail_reason = task_data.get("fail_reason")
        self.progress = task_data.get("progress")
        self.submit_time = task_data.get("submit_time")
        self.start_time = task_data.get("start_time")
        self.finish_time = task_data.get("finish_time")

    @property
    def result(self) -> Optional[str]:
        """Get the first output URL for backward compatibility."""
        return self.outputs[0] if self.outputs else None

    @property
    def progress_percent(self) -> Optional[int]:
        """Get progress as integer percentage (0-100)."""
        if self.progress:
            # Parse "100%" to 100
            try:
                return int(self.progress.rstrip('%'))
            except (ValueError, AttributeError):
                return None
        return None

    def is_completed(self) -> bool:
        """Check if the task is completed."""
        return self.status.upper() in "SUCCESS"

    def is_failed(self) -> bool:
        """Check if the task has failed."""
        return self.status.upper() in "FAILURE"

    def is_processing(self) -> bool:
        """Check if the task is still processing."""
        return self.status.upper() in ("NOT_START", "SUBMITTED", "QUEUED", "IN_PROGRESS")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.raw_response
