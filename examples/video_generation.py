"""
Example: Video generation using Siray SDK

This example demonstrates how to use the Siray SDK for video generation.
"""

import os
from siray import Siray, SirayError


# Initialize the client
client = Siray()  # Uses SIRAY_API_KEY from environment


def example_basic_video_generation():
    """Example: Basic video generation"""
    print("=== Basic Video Generation ===")

    try:
        response = client.video.generate_async(
            model="your-video-model",
            prompt="A cat playing piano in a cozy living room with warm lighting"
        )

        print("Video generation started!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")


def example_video_with_parameters():
    """Example: Video generation with custom parameters"""
    print("\n=== Video Generation with Custom Parameters ===")

    try:
        response = client.video.generate_async(
            model="your-video-model",
            prompt="Time-lapse of a flower blooming",
            duration=5,  # Video duration in seconds
            fps=24,      # Frames per second
            resolution="1920x1080",
        )

        print("Video generation started!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")


def example_cinematic_video_generation():
    """Example: Cinematic video generation"""
    print("\n=== Cinematic Video Generation ===")

    try:
        response = client.video.generate_async(
            model="your-video-model",
            prompt="A drone shot flying over a mountain range"
        )

        print("Video generation started!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")


def example_query_video_task_status():
    """Example: Query the status of an async video generation task"""
    print("\n=== Query Video Task Status ===")

    try:
        # Start an async video generation
        response = client.video.generate_async(
            model="your-video-model",
            prompt="A stunning time-lapse of clouds moving over a city skyline"
        )

        print("Video generation started!")
        print(f"Task ID: {response.task_id}")

        # Query the task status
        status = client.video.query_task(response.task_id)

        print(f"Status: {status.status}")
        print(f"Progress: {status.progress}")

        if status.is_completed():
            print(f"✓ Video generation completed successfully!")
            if status.outputs:
                print(f"  Generated {len(status.outputs)} video(s):")
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
        example_basic_video_generation()
        example_video_with_parameters()
        example_cinematic_video_generation()
        example_query_video_task_status()
