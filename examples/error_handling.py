"""
Example: Error handling with Siray SDK

This example demonstrates how to properly handle errors when using the Siray SDK.
"""

from siray import (
    Siray,
    SirayError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    APIError,
)


def example_authentication_error():
    """Example: Handling authentication errors"""
    print("=== Authentication Error Example ===")

    try:
        # Initialize with invalid API key
        client = Siray(api_key="invalid-api-key")

        result = client.image.generate_async(
            model="black-forest-labs/flux-1.1-pro-ultra-i2i",
            prompt="A beautiful landscape",
            image="https://example.com/image.jpg"
        )

    except AuthenticationError as e:
        print(f"Authentication failed: {e.message}")
        print(f"Status code: {e.status_code}")
        print("Please check your API key and try again.")


def example_bad_request_error():
    """Example: Handling bad request errors"""
    print("\n=== Bad Request Error Example ===")

    client = Siray()  # Uses valid API key from environment

    try:
        # Missing required parameter
        result = client.image.generate_async(
            model="black-forest-labs/flux-1.1-pro-ultra-i2i",
            prompt="",  # Empty prompt
            image="https://example.com/image.jpg"
        )

    except BadRequestError as e:
        print(f"Invalid request: {e.message}")
        print(f"Status code: {e.status_code}")
        if e.code:
            print(f"Error code: {e.code}")
        if e.error_type:
            print(f"Error type: {e.error_type}")


def example_comprehensive_error_handling():
    """Example: Comprehensive error handling"""
    print("\n=== Comprehensive Error Handling Example ===")

    try:
        client = Siray()  # May raise ValueError if API key not found

        result = client.image.generate_async(
            model="black-forest-labs/flux-1.1-pro-ultra-i2i",
            prompt="A futuristic city",
            image="https://example.com/image.jpg"
        )

        print("Generation successful!")
        print(f"Result: {result}")

    except ValueError as e:
        # Raised when API key is not provided
        print(f"Configuration error: {str(e)}")
        print("Please set SIRAY_API_KEY environment variable or provide api_key parameter")

    except AuthenticationError as e:
        print(f"Authentication failed: {e.message}")
        print("Your API key may be invalid or expired")

    except BadRequestError as e:
        print(f"Invalid request: {e.message}")
        if e.code:
            print(f"Error code: {e.code}")
        print("Please check your request parameters")

    except InternalServerError as e:
        print(f"Server error: {e.message}")
        print("The service is experiencing issues. Please try again later.")

    except APIError as e:
        print(f"API error: {e.message}")
        if e.status_code:
            print(f"Status code: {e.status_code}")

    except SirayError as e:
        # Catch any other Siray-specific errors
        print(f"Siray SDK error: {e.message}")

    except Exception as e:
        # Catch any unexpected errors
        print(f"Unexpected error: {str(e)}")


def example_retry_logic():
    """Example: Implementing retry logic for transient errors"""
    print("\n=== Retry Logic Example ===")

    import time

    client = Siray()
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            result = client.image.generate_async(
                model="black-forest-labs/flux-1.1-pro-ultra-i2i",
                prompt="A serene landscape",
                image="https://example.com/image.jpg"
            )

            print("Generation successful!")
            print(f"Result: {result}")
            break

        except InternalServerError as e:
            # Retry on server errors
            print(f"Attempt {attempt + 1} failed: {e.message}")

            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Giving up.")

        except (AuthenticationError, BadRequestError) as e:
            # Don't retry on client errors
            print(f"Error: {e.message}")
            print("This error cannot be resolved by retrying.")
            break


if __name__ == "__main__":
    print("Error Handling Examples\n")

    # Run examples
    example_authentication_error()
    example_bad_request_error()
    example_comprehensive_error_handling()
    example_retry_logic()
