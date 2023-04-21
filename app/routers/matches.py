from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.auth import AccessLevel, api_key_read_access_auth, api_key_write_access_auth
from app.models.matches import Match
from app.repositories.base.validators import assert_not_in
from app.repositories.matches.repo import MatchRepository
from app.repositories.matches.validators import validate_opponent_exists
from app.routers._helpers import (
    add_or_raise_http_exception,
    remove_or_raise_http_exception,
)
from app.settings.api import get_api_settings

router = APIRouter()


@router.get("")
async def list_matches(access_level: Annotated[AccessLevel, Depends(api_key_read_access_auth)]):
    """List all matches."""
    matches = MatchRepository.load().assets

    matches.sort(reverse=True)

    settings = get_api_settings()
    if access_level is AccessLevel.READ and settings.hide_spoilers:
        return matches[:5]
    return matches


@router.post(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_201_CREATED,
)
async def add_match(match: Match):
    """Add a match."""
    repo = MatchRepository.load()
    add_or_raise_http_exception(repo, match, validators={assert_not_in, validate_opponent_exists})
    return match


@router.delete(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_match(match: Match):
    """Delete a match."""
    repo = MatchRepository.load()
    remove_or_raise_http_exception(repo, match, validators=set())
    return match
