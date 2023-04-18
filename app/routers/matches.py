from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.exceptions import NotFoundError
from app.models.matches import Match
from app.repositories.base.validators import assert_in, assert_not_in
from app.repositories.matches import MatchRepository
from app.repositories.opponents import OpponentRepository
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
    try:
        assert_in(OpponentRepository.load(), match.opponent)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    match_repo = MatchRepository.load()
    add_or_raise_http_exception(match_repo, match, [assert_not_in])
    return match


@router.delete(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_match(match: Match):
    """Delete a match."""
    repo = MatchRepository.load()
    remove_or_raise_http_exception(repo, match, [])
    return match
