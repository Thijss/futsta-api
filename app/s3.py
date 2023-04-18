"""S3 bucket for assets"""
import logging
from pathlib import Path
from typing import Optional

import boto3

from app.settings.repository import get_repo_settings


class S3AssetBucket:
    """S3 bucket for assets"""

    def __init__(self, bucket_name: str, client: Optional[boto3.client] = None):
        self.s3_client = client or boto3.client("s3")
        self.bucket_name = bucket_name

    def download_asset(self, file_name: str):
        """Download asset from S3 bucket"""
        settings = get_repo_settings()

        if not settings.s3_access:
            logging.warning("Download skipped: S3 access is disabled in settings")
            return

        local_path = f"{settings.local_assets_dir}/{file_name}"
        s3_path = f"{settings.s3_assets_dir}/{file_name}"

        self.s3_client.download_file(self.bucket_name, s3_path, local_path)

    def upload_asset(self, file_name: str):
        """Upload asset to S3 bucket"""
        settings = get_repo_settings()

        if not settings.s3_access:
            logging.warning("Upload skipped: S3 access is disabled in settings")
            return

        local_path = f"{settings.local_assets_dir}/{file_name}"
        s3_path = f"{settings.s3_assets_dir}/{file_name}"

        self.s3_client.upload_file(local_path, self.bucket_name, s3_path)
