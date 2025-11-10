# Siray Python SDK

[![PyPI version](https://badge.fury.io/py/siray.svg)](https://badge.fury.io/py/siray)
[![Python version](https://img.shields.io/pypi/pyversions/siray.svg)](https://pypi.org/project/siray/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

The official Python client library for [Siray AI](https://siray.ai) - a platform for AI-powered image and video generation.

## Installation

Install the package using pip:

```bash
pip install siray
```

Or install from source:

```bash
git clone https://github.com/siray-ai/siray-python.git
cd siray-python
pip install .
```

## Quick Start

### Authentication

Get your API key from [Siray AI Dashboard](https://siray.ai/dashboard) and set it as an environment variable:

```bash
export SIRAY_API_KEY="your-api-key-here"
```

Or pass it directly when initializing the client:

```python
from siray import Siray

client = Siray(api_key="your-api-key-here")
```

### Image Generation

#### Image-to-Image (Flux 1.1 Pro Ultra I2i)

```python
from siray import Siray

client = Siray()

# Generate image asynchronously
response = client.image.generate_async(
    model="black-forest-labs/flux-1.1-pro-ultra-i2i",
    prompt="A beautiful sunset over mountains with vibrant colors",
    image="https://example.com/input-image.jpg"
)

print(f"Task ID: {response.task_id}")
```

#### Query Task Status

```python
# After starting an async generation, query its status
status = client.image.query_task(response.task_id)

if status.is_completed():
    print(f"✓ Completed!")
    for i, url in enumerate(status.outputs, 1):
        print(f"  Image {i}: {url}")
elif status.is_processing():
    print(f"⏳ Processing... {status.progress}")
elif status.is_failed():
    print(f"✗ Failed: {status.fail_reason}")
```

### Video Generation

```python
from siray import Siray

client = Siray()

# Generate video asynchronously
response = client.video.generate_async(
    model="your-video-model",
    prompt="A cat playing piano in a cozy room"
)

print(f"Task ID: {response.task_id}")
```

## API Reference

### Client

#### `Siray(api_key=None, base_url="https://api.siray.ai")`

Main client for interacting with Siray AI API.

**Parameters:**
- `api_key` (str, optional): API key for authentication. If not provided, reads from `SIRAY_API_KEY` environment variable.
- `base_url` (str, optional): Base URL for the API. Default: `https://api.siray.ai`

**Attributes:**
- `image`: Image generation namespace
- `video`: Video generation namespace

### Image

#### `image.generate_async(model, prompt, image, **kwargs)`

Generate an image asynchronously using image-to-image models.

**Parameters:**
- `model` (str): Model identifier (e.g., `"black-forest-labs/flux-1.1-pro-ultra-i2i"`)
- `prompt` (str): Text prompt for image generation
- `image` (str): Input image (URL or base64 encoded string)
- `**kwargs`: Additional model-specific parameters

**Returns:** `GenerationResponse` object with the following attributes:
- `task_id` (str): Unique identifier for the generation task
- `raw_response` (dict): Raw API response data

#### `image.query_task(task_id)`

Query the status and result of an image generation task.

**Parameters:**
- `task_id` (str): Task ID returned from the image generation request

**Returns:** `TaskStatus` object with the following attributes:
- `code` (str): Response code (e.g., 'success')
- `message` (str): Response message
- `task_id` (str): Task identifier
- `action` (str): Action type (e.g., 'imageGenerate')
- `status` (str): Current task status (e.g., 'SUCCESS', 'PENDING', 'FAILED')
- `outputs` (List[str]): List of output URLs
- `fail_reason` (str | None): Failure reason if task failed
- `progress` (str | None): Progress string (e.g., '100%')
- `submit_time` (int | None): Unix timestamp when submitted
- `start_time` (int | None): Unix timestamp when started
- `finish_time` (int | None): Unix timestamp when finished
- `result` (property): First output URL (for backward compatibility)
- `progress_percent` (property): Progress as integer (0-100)
- `is_completed()` (method): Check if task is completed
- `is_processing()` (method): Check if task is still processing
- `is_failed()` (method): Check if task has failed

**Example:**
```python
# Start async generation
response = client.image.generate_async(
    model="black-forest-labs/flux-kontext-i2i-max",
    prompt="A beautiful sunset",
    image="https://example.com/input.jpg"
)

# Query task status
status = client.image.query_task(response.task_id)

if status.is_completed():
    print(f"Generated {len(status.outputs)} image(s)")
    for url in status.outputs:
        print(f"  - {url}")
elif status.is_failed():
    print(f"Error: {status.fail_reason}")
```

### Video

#### `video.generate_async(model, prompt, **kwargs)`

Generate a video asynchronously.

**Parameters:**
- `model` (str): Model identifier
- `prompt` (str): Text prompt for video generation
- `**kwargs`: Additional model-specific parameters (e.g., duration, fps)

**Returns:** `GenerationResponse` object with the following attributes:
- `task_id` (str): Unique identifier for the generation task
- `raw_response` (dict): Raw API response data

#### `video.query_task(task_id)`

Query the status and result of a video generation task.

**Parameters:**
- `task_id` (str): Task ID returned from the video generation request

**Returns:** `TaskStatus` object (same structure as image query)

**Example:**
```python
# Start async generation
response = client.video.generate_async(
    model="your-video-model",
    prompt="A cat playing piano"
)

# Query task status
status = client.video.query_task(response.task_id)

if status.is_completed():
    print(f"Generated {len(status.outputs)} video(s)")
    for url in status.outputs:
        print(f"  - {url}")
elif status.is_failed():
    print(f"Error: {status.fail_reason}")
```

## Response Models

The SDK provides typed response objects instead of raw dictionaries:

### `GenerationResponse`

Returned by `generate_async()` methods. Contains:
- `task_id`: Unique task identifier
- `raw_response`: Raw API response data
- `to_dict()`: Convert to dictionary

### `TaskStatus`

Returned by `query_task()` method. Contains:
- `code`: Response code (e.g., 'success')
- `message`: Response message
- `task_id`: Task identifier
- `action`: Action type (e.g., 'imageGenerate')
- `status`: Current status (e.g., 'SUCCESS', 'PENDING', 'FAILED')
- `outputs`: List of output URLs
- `fail_reason`: Failure reason if task failed
- `progress`: Progress string (e.g., '100%')
- `submit_time`: Unix timestamp when submitted
- `start_time`: Unix timestamp when started
- `finish_time`: Unix timestamp when finished
- `result` (property): First output URL (backward compatibility)
- `progress_percent` (property): Progress as integer (0-100)
- `is_completed()`: Check if completed
- `is_processing()`: Check if processing
- `is_failed()`: Check if failed
- `to_dict()`: Convert to dictionary

## Error Handling

The SDK provides specific exception classes for different error scenarios:

```python
from siray import Siray, SirayError, AuthenticationError, BadRequestError

client = Siray()

try:
    result = client.image.generate_async(
        model="black-forest-labs/flux-1.1-pro-ultra-i2i",
        prompt="A beautiful sunset",
        image="https://example.com/image.jpg"
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
except BadRequestError as e:
    print(f"Invalid request: {e.message}")
    print(f"Error code: {e.code}")
    print(f"Error type: {e.error_type}")
except SirayError as e:
    print(f"API error: {e.message}")
    print(f"Status code: {e.status_code}")
```

### Exception Types

- `SirayError`: Base exception for all SDK errors
- `AuthenticationError`: Raised when authentication fails (401)
- `BadRequestError`: Raised when the request is invalid (400)
- `InternalServerError`: Raised when the server encounters an error (500)
- `APIError`: Raised for general API errors

## Examples

See the [examples](examples/) directory for more comprehensive usage examples:

- [Basic image generation](examples/image_generation.py)
- [Video generation](examples/video_generation.py)
- [Error handling](examples/error_handling.py)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/siray-ai/siray-python.git
cd siray-python

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install .
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
# Format code
black siray/

# Check code style
flake8 siray/

# Sort imports
isort siray/

# Type checking
mypy siray/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://docs.siray.ai
- API Reference: https://docs.siray.ai/api-reference/
- Issues: https://github.com/siray-ai/siray-python/issues
- Email: support@siray.ai

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each release.