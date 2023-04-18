"""S3 bucket for assets"""
import logging
from pathlib import PosixPath

import boto3

from app.settings.repository import FileAccess, get_repo_settings


class S3AssetBucket:
    """S3 bucket for assets"""

    def __init__(self, bucket_name: str):
        self.s3_client = boto3.client("s3")
        self.bucket_name = bucket_name

    def download_asset(self, file_name: PosixPath):
        """Download asset from S3 bucket"""
        settings = get_repo_settings()

        if settings.s3_access is FileAccess.NO_ACCESS:
            logging.warning("Download skipped: S3 access is disabled in settings")
            return

        local_path = f"{settings.local_assets_dir}/{file_name}"
        s3_path = f"{settings.s3_assets_dir}/{file_name}"

        self.s3_client.download_file(self.bucket_name, s3_path, local_path)

    def upload_asset(self, file_name: PosixPath):
        """Upload asset to S3 bucket"""
        settings = get_repo_settings()

        if settings.s3_access is not FileAccess.WRITE:
            logging.warning("Upload skipped: S3 access is disabled in settings")
            return

        local_path = f"{settings.local_assets_dir}/{file_name}"
        s3_path = f"{settings.s3_assets_dir}/{file_name}"

        self.s3_client.upload_file(local_path, self.bucket_name, s3_path)
