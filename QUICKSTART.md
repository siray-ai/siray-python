# Quick Start Guide

This guide will help you get started with the Siray Python SDK in 5 minutes.

## Installation

```bash
pip install siray
```

## Get Your API Key

1. Go to [Siray AI Dashboard](https://siray.ai/dashboard)
2. Create an account or log in
3. Navigate to API Keys section
4. Copy your API key

## Set Up Authentication

### Option 1: Environment Variable (Recommended)

```bash
export SIRAY_API_KEY="your-api-key-here"
```

Add this to your `~/.bashrc` or `~/.zshrc` to make it permanent.

### Option 2: Pass Directly in Code

```python
from siray import Siray

client = Siray(api_key="your-api-key-here")
```

## Your First Image Generation

### Image-to-Image Generation

```python
from siray import Siray

# Initialize client
client = Siray()  # Uses SIRAY_API_KEY from environment

# Generate an image
result = client.image.generate_async(
    model="black-forest-labs/flux-1.1-pro-ultra-i2i",
    prompt="A beautiful sunset over mountains with vibrant colors",
    image="https://example.com/your-input-image.jpg"
)

print(result)
```

## Your First Video Generation

```python
from siray import Siray

client = Siray()

result = client.video.generate_async(
    model="your-video-model",
    prompt="A cat playing piano in a cozy room"
)

print(result)
```

## Error Handling

Always wrap your API calls in try-except blocks:

```python
from siray import Siray, SirayError, AuthenticationError, BadRequestError

client = Siray()

try:
    result = client.image.generate_async(
        model="black-forest-labs/flux-1.1-pro-ultra-i2i",
        prompt="A beautiful sunset",
        image="https://example.com/image.jpg"
    )
    print("Success:", result)

except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")

except BadRequestError as e:
    print(f"Invalid request: {e.message}")

except SirayError as e:
    print(f"API error: {e.message}")
```

## Common Parameters

Most generation methods accept these common parameters:

- `model` (required): The model identifier
- `prompt` (required): Your text description
- `image` (optional): Input image for image-to-image models
- **Additional model-specific parameters** via `**kwargs`

Example with custom parameters:

```python
result = client.image.generate_async(
    model="black-forest-labs/flux-1.1-pro-ultra-i2i",
    prompt="A futuristic city at night",
    image="https://example.com/city.jpg",
    aspect_ratio="16:9",
    seed=42,
)
```

## Next Steps

- Read the full [README](README.md) for complete documentation
- Check out [examples](examples/) directory for more use cases
- Visit [Siray AI Documentation](https://docs.siray.ai) for API details
- Join our community for support

## Troubleshooting

### "API key must be provided" Error

Make sure you've either:
- Set the `SIRAY_API_KEY` environment variable, or
- Passed `api_key` parameter when creating the client

### Authentication Failed (401)

- Check that your API key is correct
- Verify it hasn't expired
- Ensure you're using the key from the correct environment (dev/production)

### Bad Request (400)

- Verify all required parameters are provided
- Check that parameter values are valid
- Ensure image URLs are accessible

## Getting Help

- Documentation: https://docs.siray.ai
- Issues: https://github.com/siray-ai/siray-python/issues
- Email: support@siray.ai
