"""S3 uploader with support for multipart uploads."""

import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


class S3Uploader:
    """Handle S3 uploads with automatic multipart support for large files."""

    # 8MB threshold and chunk size
    MULTIPART_THRESHOLD = 8 * 1024 * 1024  # 8MB
    CHUNK_SIZE = 8 * 1024 * 1024  # 8MB

    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        session_token: str,
        region: str,
        bucket_name: str,
        endpoint_url: Optional[str] = None,
        access_endpoint: Optional[str] = None,
    ):
        """
        Initialize S3 uploader with temporary credentials.

        Args:
            access_key_id: AWS access key ID from STS token
            secret_access_key: AWS secret access key from STS token
            session_token: AWS session token from STS token
            region: AWS region
            bucket_name: S3 bucket name
            endpoint_url: Optional custom S3 endpoint URL for upload
            access_endpoint: Optional custom S3 endpoint URL for access

        Raises:
            ImportError: If boto3 is not installed
        """
        if not HAS_BOTO3:
            raise ImportError(
                "boto3 is required for file uploads. "
                "Install it with: pip install boto3"
            )

        self.bucket_name = bucket_name
        self.region = region
        self.access_endpoint = access_endpoint

        # Create S3 client configuration for UCloud US3 compatibility
        from botocore.client import Config

        config = Config(
            signature_version='s3v4',
            s3={'addressing_style': 'path'}
        )

        # Create S3 client with temporary credentials
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            region_name=region,
            endpoint_url=endpoint_url,
            config=config,
            verify=False,  # Disable SSL verification for UCloud US3
        )

    def upload_file(
        self,
        file_path: str,
        object_key: str,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload a file to S3 with automatic multipart support.

        Args:
            file_path: Path to the local file to upload
            object_key: S3 object key (path in bucket)
            content_type: Optional MIME type of the file

        Returns:
            S3 URL of the uploaded file

        Raises:
            FileNotFoundError: If file_path does not exist
            ClientError: If S3 upload fails
        """
        path = Path(file_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = path.stat().st_size

        # Determine upload strategy based on file size
        if file_size > self.MULTIPART_THRESHOLD:
            return self._multipart_upload(path, object_key, content_type)
        else:
            return self._simple_upload(path, object_key, content_type)

    def _simple_upload(
        self,
        file_path: Path,
        object_key: str,
        content_type: Optional[str] = None,
    ) -> str:
        """Upload file using simple PUT operation."""
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        with open(file_path, "rb") as f:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=f,
                **extra_args,
            )

        return self._get_object_url(object_key)

    def _multipart_upload(
        self,
        file_path: Path,
        object_key: str,
        content_type: Optional[str] = None,
    ) -> str:
        """Upload file using multipart upload for large files."""
        # Initiate multipart upload
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        mpu = self.s3_client.create_multipart_upload(
            Bucket=self.bucket_name,
            Key=object_key,
            **extra_args,
        )
        upload_id = mpu["UploadId"]

        parts = []
        part_number = 1

        try:
            with open(file_path, "rb") as f:
                while True:
                    # Read chunk
                    data = f.read(self.CHUNK_SIZE)
                    if not data:
                        break

                    # Upload part
                    response = self.s3_client.upload_part(
                        Bucket=self.bucket_name,
                        Key=object_key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=data,
                    )

                    parts.append({
                        "PartNumber": part_number,
                        "ETag": response["ETag"],
                    })

                    part_number += 1

            # Complete multipart upload
            self.s3_client.complete_multipart_upload(
                Bucket=self.bucket_name,
                Key=object_key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )

        except Exception as e:
            # Abort multipart upload on error
            self.s3_client.abort_multipart_upload(
                Bucket=self.bucket_name,
                Key=object_key,
                UploadId=upload_id,
            )
            raise e

        return self._get_object_url(object_key)

    def _get_object_url(self, object_key: str) -> str:
        """Get the URL for an uploaded object."""
        # Use access_endpoint if provided
        if self.access_endpoint:
            # Ensure the endpoint has protocol
            endpoint = self.access_endpoint
            if not endpoint.startswith('http://') and not endpoint.startswith('https://'):
                endpoint = f"https://{endpoint}"
            # Construct URL with object key
            return f"{endpoint.rstrip('/')}/{object_key}"

        # Handle custom endpoint from upload
        try:
            if self.s3_client._endpoint and hasattr(self.s3_client._endpoint, 'host'):
                endpoint = self.s3_client._endpoint.host
                # For UCloud US3 and other S3-compatible services
                # URL format: https://{endpoint}/{object_key}
                return f"https://{endpoint}/{object_key}"
        except:
            pass

        # Fallback: construct URL from bucket and region
        return f"https://{self.bucket_name}.{self.region}.ufileos.com/{object_key}"
