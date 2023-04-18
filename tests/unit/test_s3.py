"""Unit tests for the S3 module."""
# pylint: disable=missing-function-docstring
import os
from unittest.mock import Mock, patch

from app.s3 import S3AssetBucket


def test_download_no_access():
    client = Mock()
    file_name = "test-file"

    bucket = S3AssetBucket(bucket_name="test-bucket", client=client)

    bucket.download_asset(file_name)
    bucket.upload_asset(file_name)

    assert client.download_file.call_count == 0


def test_download_with_access():
    client = Mock()
    file_name = "test-file"

    bucket = S3AssetBucket(bucket_name="test-bucket", client=client)

    with patch.dict(os.environ, {"S3_ACCESS": "True"}):
        bucket.download_asset(file_name)
        bucket.upload_asset(file_name)

    assert client.download_file.call_count == 1
    assert client.upload_file.call_count == 1
