"""Setup script for Siray Python SDK."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="siray",
    version="0.1.0",
    author="Siray AI",
    author_email="support@siray.ai",
    description="Python client library for Siray AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/siray-ai/siray-python",
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "httpx>=0.24.0",
        "requests>=2.28.0",  # Fallback if httpx not available
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/siray-ai/siray-python/issues",
        "Source": "https://github.com/siray-ai/siray-python",
        "Documentation": "https://docs.siray.ai",
    },
)
