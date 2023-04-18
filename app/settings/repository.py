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
    if profile := os.getenv("SETTINGS_PROFILE"):
        settings_profile = SettingsProfile(profile)
    else:
        return RepositorySettings()

    if settings_profile in [SettingsProfile.AWS_LAMBDA_DEV, SettingsProfile.AWS_LAMBDA_PRD]:
        return _get_lambda_settings()
    if settings_profile is SettingsProfile.LOCAL:
        return _get_local_settings()
    raise NotImplementedError(f"Settings profile {settings_profile} not implemented")


@lru_cache()
def _get_lambda_settings():
    return RepositorySettings(
        local_access=True,
        s3_access=True,
    )


@lru_cache
def _get_local_settings():
    return RepositorySettings(
        local_access=True,
        s3_access=False,
    )
