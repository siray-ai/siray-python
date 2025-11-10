"""Example: Blocking generation using the `run` helper methods."""

import os
from siray import Siray, SirayError


client = Siray()  # Uses SIRAY_API_KEY from environment


def run_image_generation():
    """Start an image task and wait until it finishes."""
    print("=== Blocking Image Generation ===")
    try:
        status = client.image.run(
            model="black-forest-labs/flux-1.1-pro-ultra-i2i",
            prompt="A retro robot sketch on blueprint paper",
            image="https://example.com/input.png",
            poll_interval=2.0,
            timeout=120,
        )
        print(f"Final status: {status.status}")
        if status.is_completed():
            for url in status.outputs:
                print(f"  Output: {url}")
        elif status.is_failed():
            print(f"Failed: {status.fail_reason}")
    except TimeoutError as e:
        print(f"Timed out: {e}")
    except SirayError as e:
        print(f"API error: {e.message}")


def run_video_generation():
    """Start a video task and block for completion."""
    print("\n=== Blocking Video Generation ===")
    try:
        status = client.video.run(
            model="your-video-model",
            prompt="A drone flythrough of a neon city",
            poll_interval=3.0,
            timeout=300,
        )
        print(f"Final status: {status.status}")
        if status.is_completed():
            for url in status.outputs:
                print(f"  Output: {url}")
        elif status.is_failed():
            print(f"Failed: {status.fail_reason}")
    except TimeoutError as e:
        print(f"Timed out: {e}")
    except SirayError as e:
        print(f"API error: {e.message}")


if __name__ == "__main__":
    if not os.environ.get("SIRAY_API_KEY"):
        print("Warning: SIRAY_API_KEY environment variable not set")
        print("Set it with: export SIRAY_API_KEY='your-api-key'")
    else:
        run_image_generation()
        run_video_generation()
