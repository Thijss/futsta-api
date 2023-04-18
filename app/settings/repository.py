"""Repository settings."""
import os
from functools import lru_cache

from pydantic import BaseSettings

from app.settings._enums import SettingsProfile


class RepositorySettings(BaseSettings):
    """Repository settings."""

    def __str__(self):
        setting_list = [f"[Settings parameter] {key}: {value}" for key, value in sorted(self.dict().items())]
        lines = ["---------- SETTINGS ----------"] + setting_list
        return os.linesep.join(lines)

    local_assets_dir: str = "assets"
    local_access: bool = False
    s3_assets_dir: str = "assets"
    s3_access: bool = False
    s3_bucket_name: str = ""

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_prefix = ""
        env_file_encoding = "utf-8"


def get_repo_settings():
    """Get API settings."""
    if os.getenv("USE_LAMBDA_DEV_SETTINGS"):
        return _get_lambda_dev_settings()

    if os.getenv("USE_LRU_CACHED_SETTINGS"):
        return _get_cached_settings()

    return RepositorySettings()


@lru_cache()
def _get_lambda_dev_settings():
    return RepositorySettings(
        local_access=True,
        s3_access=True,
    )


@lru_cache
def _get_cached_settings():
    return RepositorySettings()
