"""
Example: 3D model generation using Siray SDK

This example demonstrates how to use the Siray SDK for 3D model generation,
including both text-to-3D and image-to-3D workflows.
"""

import os
from siray import Siray, SirayError


# Initialize the client
client = Siray()  # Uses SIRAY_API_KEY from environment


def example_text_to_3d():
    """Example: Text-to-3D generation"""
    print("=== Text-to-3D Generation ===")

    try:
        response = client.generation_3d.generate_async(
            model="tencent/hunyuan3d-v2.5-rapid-text-to-3d",
            prompt="A cute cartoon cat sitting on a table",
            pbr_enable=True,
            texture_enable=True,
        )

        print("3D generation started!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")


def example_image_to_3d():
    """Example: Image-to-3D generation"""
    print("\n=== Image-to-3D Generation ===")

    try:
        response = client.generation_3d.generate_async(
            model="tencent/hunyuan3d-v2.5-rapid-image-to-3d",
            image="https://example.com/cat.png",
            pbr_enable=True,
            texture_enable=True,
        )

        print("3D generation started!")
        print(f"Task ID: {response.task_id}")

    except SirayError as e:
        print(f"Error: {e.message}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")


def example_blocking_text_to_3d():
    """Example: Blocking text-to-3D generation (poll until complete)"""
    print("\n=== Blocking Text-to-3D Generation ===")

    try:
        status = client.generation_3d.run(
            model="tencent/hunyuan3d-v2.5-rapid-text-to-3d",
            prompt="A medieval sword with ornate handle",
            pbr_enable=True,
            texture_enable=True,
            poll_interval=3.0,
            timeout=300,
        )

        if status.is_completed():
            print("3D generation completed!")
            if status.outputs:
                print(f"Generated {len(status.outputs)} asset(s):")
                for i, url in enumerate(status.outputs, 1):
                    print(f"  {i}. {url}")
        elif status.is_failed():
            print(f"Failed: {status.fail_reason}")

    except TimeoutError as e:
        print(f"Timeout: {e}")
    except SirayError as e:
        print(f"Error: {e.message}")


def example_query_3d_task_status():
    """Example: Query the status of an async 3D generation task"""
    print("\n=== Query 3D Task Status ===")

    try:
        # Start an async generation
        response = client.generation_3d.generate_async(
            model="tencent/hunyuan3d-v2.5-rapid-text-to-3d",
            prompt="A wooden treasure chest",
        )

        print(f"Task ID: {response.task_id}")

        # Query the task status
        status = client.generation_3d.query_task(response.task_id)

        print(f"Status: {status.status}")
        print(f"Progress: {status.progress}")

        if status.is_completed():
            print("3D generation completed!")
            if status.outputs:
                print(f"  Generated {len(status.outputs)} asset(s):")
                for i, url in enumerate(status.outputs, 1):
                    print(f"  {i}. {url}")
        elif status.is_processing():
            print("Processing...")
        elif status.is_failed():
            print(f"Failed: {status.fail_reason}")

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
        example_text_to_3d()
        example_image_to_3d()
        example_blocking_text_to_3d()
        example_query_3d_task_status()
