from fastapi import APIRouter, Depends
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.models.matches import Match
from app.repositories.base.validators import assert_not_in
from app.repositories.matches.repo import MatchRepository
from app.repositories.matches.validators import validate_opponent_exists
from app.routers._helpers import add_or_raise_http_exception, remove_or_raise_http_exception

router = APIRouter()


@router.get("", dependencies=[Depends(api_key_read_access_auth)])
async def list_matches():
    """List all matches."""
    matches = MatchRepository.load().assets
    matches.sort()
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
