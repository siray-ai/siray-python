"""
Example: File Upload

This example demonstrates how to upload files to Siray storage using the SDK.
Files larger than 8MB are automatically uploaded using multipart upload.
"""

from siray import Siray


def main():
    # Initialize client
    client = Siray()

    print("=" * 60)
    print("File Upload Example")
    print("=" * 60)

    # Example 1: Upload an image file
    print("\n1. Upload an image file")
    print("-" * 60)

    file_path = "path/to/your/image.jpg"

    try:
        # Upload file and get URL
        url = client.files.upload(file_path)
        print(f"✓ File uploaded successfully!")
        print(f"  URL: {url}")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("  Please update the file_path variable with a valid file path")
    except Exception as e:
        print(f"✗ Upload failed: {e}")

    # Example 2: Upload large file (multipart upload will be used automatically)
    print("\n2. Upload large file (>8MB)")
    print("-" * 60)
    print("  For files larger than 8MB, the SDK automatically uses")
    print("  multipart upload with 8MB chunks for better performance.")

    large_file_path = "path/to/large/video.mp4"

    try:
        url = client.files.upload(large_file_path)
        print(f"✓ Large file uploaded successfully!")
        print(f"  URL: {url}")
    except FileNotFoundError:
        print("  (Skipped - no large file specified)")
    except Exception as e:
        print(f"✗ Upload failed: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
