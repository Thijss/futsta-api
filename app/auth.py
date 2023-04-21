"""Authentication and authorization for the API."""
from enum import IntEnum, auto

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.settings.api import get_api_settings

api_key_header = APIKeyHeader(name="ApiKey", auto_error=False)


class AccessLevel(IntEnum):
    """Enum for access levels."""

    READ = auto()
    WRITE = auto()


async def api_key_read_access_auth(api_key: str = Security(api_key_header)):
    """Check if the API key is valid for read-only access."""
    api_settings = get_api_settings()

    required_api_keys = [
        api_settings.api_key_read_access.get_secret_value(),
        api_settings.api_key_write_access.get_secret_value(),
    ]
    if api_key == "" or api_key not in required_api_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

    if api_key == api_settings.api_key_write_access.get_secret_value():
        return AccessLevel.WRITE
    return AccessLevel.READ


async def api_key_write_access_auth(api_key: str = Security(api_key_header)):
    """Check if the API key is valid for full access."""
    settings = get_api_settings()
    if api_key == "" or api_key != settings.api_key_write_access.get_secret_value():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")
