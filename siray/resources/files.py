"""File upload resource for Siray SDK."""

import mimetypes
import os
from pathlib import Path

from ..base_client import BaseClient
from ..upload.s3_uploader import S3Uploader


class Files:
    """
    Files resource for uploading files to Siray storage.

    This resource handles file uploads using S3 protocol with temporary
    STS credentials. Files larger than 8MB are automatically uploaded
    using multipart upload.
    """

    def __init__(self, client: BaseClient):
        """
        Initialize the Files resource.

        Args:
            client: Base client instance for making API requests
        """
        self._client = client

    def _get_sts_token(self) -> dict:
        """
        Fetch STS token from the API.

        Returns:
            Dictionary containing credentials, bucket_name, upload_path, and endpoint

        Raises:
            APIError: If the API request fails
        """
        response = self._client.post("/api/model-verse/sts-token")

        # Extract data from response
        data = response.get("data", {})
        if not data:
            raise ValueError("Invalid STS token response: missing data field")

        return data

    def upload(self, file_path: str) -> str:
        """
        Upload a file to Siray storage.

        Files larger than 8MB are automatically uploaded using multipart upload
        with 8MB chunks. Smaller files use simple PUT upload.

        Args:
            file_path: Path to the local file to upload

        Returns:
            URL of the uploaded file

        Raises:
            FileNotFoundError: If file_path does not exist
            ImportError: If boto3 is not installed
            APIError: If STS token request or upload fails

        Example:
            >>> from siray import Siray
            >>> client = Siray(api_key="your-api-key")
            >>>
            >>> # Upload a file
            >>> url = client.files.upload("path/to/image.jpg")
            >>> print(f"Uploaded to: {url}")
        """
        # Validate file exists
        path = Path(file_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get STS token
        sts_data = self._get_sts_token()

        credentials = sts_data.get("credentials", {})
        bucket_name = sts_data.get("bucket_name")
        upload_path = sts_data.get("upload_path", "")
        endpoint = sts_data.get("endpoint")

        if not credentials or not bucket_name:
            raise ValueError("Invalid STS token response: missing credentials or bucket_name")

        # Determine object key using upload_path + filename
        filename = path.name
        object_key = os.path.join(upload_path, filename).replace("\\", "/")

        # Infer content type from file extension
        content_type, _ = mimetypes.guess_type(str(path))

        # Create S3 uploader with temporary credentials
        uploader = S3Uploader(
            access_key_id=credentials.get("access_key_id"),
            secret_access_key=credentials.get("secret_access_key"),
            session_token=credentials.get("session_token"),
            region=credentials.get("region", "us-east-1"),
            bucket_name=bucket_name,
            endpoint_url=endpoint,
        )

        # Upload file
        return uploader.upload_file(
            file_path=str(path),
            object_key=object_key,
            content_type=content_type,
        )
