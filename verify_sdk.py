#!/usr/bin/env python3
"""
Simple script to verify the Siray SDK installation and basic functionality.
"""

import sys


def verify_imports():
    """Verify that all SDK components can be imported."""
    print("Testing SDK imports...")

    try:
        from siray import Siray
        print("  ✓ Siray client imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import Siray: {e}")
        return False

    try:
        from siray import (
            SirayError,
            AuthenticationError,
            BadRequestError,
            InternalServerError,
            APIError,
        )
        print("  ✓ Exception classes imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import exceptions: {e}")
        return False

    try:
        import siray
        version = siray.__version__
        print(f"  ✓ SDK version: {version}")
    except Exception as e:
        print(f"  ✗ Failed to get version: {e}")
        return False

    return True


def verify_client_creation():
    """Verify that the client can be created."""
    print("\nTesting client creation...")

    try:
        from siray import Siray

        # Test with explicit API key
        client = Siray(api_key="test-api-key")
        print("  ✓ Client created with API key")

        # Verify namespaces exist
        assert hasattr(client, "image"), "Missing image namespace"
        assert hasattr(client, "video"), "Missing video namespace"
        print("  ✓ Image and video namespaces exist")

        # Verify namespace methods
        assert hasattr(client.image, "generate_async"), "Missing image.generate_async"
        assert hasattr(client.image, "query_task"), "Missing image.query_task"
        assert hasattr(client.image, "run"), "Missing image.run"
        assert hasattr(client.video, "generate_async"), "Missing video.generate_async"
        assert hasattr(client.video, "query_task"), "Missing video.query_task"
        assert hasattr(client.video, "run"), "Missing video.run"
        print("  ✓ All required methods exist")

        return True

    except Exception as e:
        print(f"  ✗ Client creation failed: {e}")
        return False


def verify_exception_hierarchy():
    """Verify exception hierarchy."""
    print("\nTesting exception hierarchy...")

    try:
        from siray import (
            SirayError,
            AuthenticationError,
            BadRequestError,
            InternalServerError,
            APIError,
        )

        # Test inheritance
        assert issubclass(AuthenticationError, SirayError), "AuthenticationError inheritance"
        assert issubclass(BadRequestError, SirayError), "BadRequestError inheritance"
        assert issubclass(InternalServerError, SirayError), "InternalServerError inheritance"
        assert issubclass(APIError, SirayError), "APIError inheritance"
        print("  ✓ Exception hierarchy correct")

        # Test exception creation
        error = BadRequestError("Test error", code="test_code", error_type="test_type")
        assert error.message == "Test error"
        assert error.code == "test_code"
        assert error.error_type == "test_type"
        print("  ✓ Exception creation works correctly")

        return True

    except Exception as e:
        print(f"  ✗ Exception verification failed: {e}")
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Siray SDK Verification")
    print("=" * 60)

    results = []

    results.append(("Imports", verify_imports()))
    results.append(("Client Creation", verify_client_creation()))
    results.append(("Exception Hierarchy", verify_exception_hierarchy()))

    print("\n" + "=" * 60)
    print("Verification Results")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✓ All verification tests passed!")
        print("\nNext steps:")
        print("1. Set your API key: export SIRAY_API_KEY='your-api-key'")
        print("2. Install the SDK: pip install .")
        print("3. Try the examples: python examples/image_generation.py")
        return 0
    else:
        print("\n✗ Some verification tests failed.")
        print("Please check the errors above and fix them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
