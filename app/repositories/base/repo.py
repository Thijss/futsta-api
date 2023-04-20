"""Base class for repositories"""
import json
from abc import ABC
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from app.repositories.base.validators import assert_in
from app.s3 import S3AssetBucket
from app.settings.repository import get_repo_settings


class JsonRepository(BaseModel, ABC):
    """Base class for repositories that store data in json files"""

    assets: list[BaseModel] = []

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config"""

        json_file_name: str

    def add(self, asset: BaseModel, validators: Optional[set[callable]] = None):
        """Add asset to repository"""
        validators = validators or []

        self._validate(asset, validators)

        self.assets.append(asset)
        self.save()

    def remove(self, asset: BaseModel, validators: Optional[set[callable]] = None):
        """Remove asset from repository"""
        validators = validators or set()
        validators.add(assert_in)

        self._validate(asset, validators)

        self.assets.remove(asset)
        self.save()

    @classmethod
    def load(cls, refresh: bool = False):
        """Load model from json"""
        settings = get_repo_settings()

        if not settings.local_access:
            raise PermissionError("No local access")

        repo = cls()
        repo._download()

        if repo.json_exists():
            json_data = repo._read_json_data()
            return cls(**json_data)
        return cls()

    def save(self):
        """Save model to json"""
        settings = get_repo_settings()
        if settings.local_access:
            self._write_json_data()
            self._upload()

    def json_exists(self):
        """Check if json file exists"""
        return Path(self.local_json_file).exists()

    @property
    def local_json_file(self) -> Path:
        """Get local json file path"""
        settings = get_repo_settings()
        return settings.local_assets_dir / self.Config.json_file_name

    def _validate(self, asset: BaseModel, validators: set[callable]):
        """Validate asset"""
        for validator in validators:
            validator(asset, self)

    def _read_json_data(self):
        with open(self.local_json_file, "r", encoding="utf-8") as infile:
            return json.load(infile)

    def _write_json_data(self):
        self.local_json_file.touch(exist_ok=True)
        with open(self.local_json_file, "w", encoding="utf-8") as outfile:
            outfile.write(self.json(indent=4))

    def _upload(self):
        settings = get_repo_settings()
        s3_bucket = S3AssetBucket(bucket_name=settings.s3_bucket_name)
        s3_bucket.upload_asset(self.Config.json_file_name)

    def _download(self):
        settings = get_repo_settings()
        s3_bucket = S3AssetBucket(bucket_name=settings.s3_bucket_name)
        s3_bucket.download_asset(self.Config.json_file_name)
