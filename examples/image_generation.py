"""
Example: Basic image generation using Siray SDK

This example demonstrates how to use the Siray SDK for image generation,
including both text-to-image and image-to-image generation.
"""

import os
from siray import Siray, SirayError

# Initialize the client
# API key can be set via SIRAY_API_KEY environment variable
# or passed directly to the constructor
client = Siray()  # Uses SIRAY_API_KEY from environment
# Or: client = Siray(api_key="your-api-key")


def example_image_to_image():
    """Example: Image-to-image generation using Flux 1.1 Pro Ultra I2i"""
    print("=== Image-to-Image Generation ===")

    try:
        response = client.image.generate_async(
            model="black-forest-labs/flux-1.1-pro-ultra-i2i",
            prompt="Transform this into a watercolor painting style",
            image="https://example.com/input-image.jpg"
        )

        print("Generation successful!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")


def example_text_to_image():
    """Example: Text-to-image generation"""
    print("\n=== Text-to-Image Generation ===")

    try:
        response = client.image.generate_async(
            model="black-forest-labs/flux-1.1-pro",
            prompt="A serene mountain landscape at sunset with a crystal clear lake, "
                   "pine trees in the foreground, and snow-capped peaks in the distance",
            image="https://example.com/input-image.jpg"
        )

        print("Generation successful!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")


def example_with_custom_parameters():
    """Example: Image generation with custom parameters"""
    print("\n=== Image Generation with Custom Parameters ===")

    try:
        response = client.image.generate_async(
            model="black-forest-labs/flux-1.1-pro-ultra-i2i",
            prompt="A futuristic cityscape at night",
            image="https://example.com/city-photo.jpg",
            # Add any custom parameters supported by the model
            aspect_ratio="16:9",
            seed=42,
        )

        print("Generation successful!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")


def example_query_task_status():
    """Example: Query the status of an async image generation task"""
    print("\n=== Query Task Status ===")

    try:
        # Start an async image generation
        response = client.image.generate_async(
            model="black-forest-labs/flux-kontext-i2i-max",
            prompt="A majestic eagle flying over mountains",
            image="https://example.com/eagle-photo.jpg"
        )

        print("Task started!")
        print(f"Task ID: {response.task_id}")

        # Query the task status
        status = client.image.query_task(response.task_id)

        print(f"Status: {status.status}")
        print(f"Progress: {status.progress}")

        if status.is_completed():
            print(f"✓ Task completed successfully!")
            if status.outputs:
                print(f"  Generated {len(status.outputs)} image(s):")
                for i, url in enumerate(status.outputs, 1):
                    print(f"  {i}. {url}")
        elif status.is_processing():
            print(f"⏳ Processing...")
        elif status.is_failed():
            print(f"✗ Failed: {status.fail_reason}")

    except SirayError as e:
        print(f"Error: {e.message}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")


if __name__ == "__main__":
    # Check if API key is set
    if not os.environ.get("SIRAY_API_KEY"):
        print("Warning: SIRAY_API_KEY environment variable not set")
        print("Set it with: export SIRAY_API_KEY='your-api-key'")
    else:
        # Run examples
        example_image_to_image()
        example_text_to_image()
        example_with_custom_parameters()
        example_query_task_status()
