from fastapi import APIRouter, Depends
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.models.opponents import Opponent
from app.repositories.base.validators import assert_not_in
from app.repositories.opponents import OpponentRepository
from app.routers._helpers import add_or_raise_http_exception

router = APIRouter()


@router.post(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_201_CREATED,
)
async def add_opponent(opponent: Opponent):
    """Add an opponent."""
    repo = OpponentRepository.load()
    add_or_raise_http_exception(repo, opponent, {assert_not_in})
    return opponent


@router.get("", dependencies=[Depends(api_key_read_access_auth)])
async def list_opponents():
    """List all opponents."""
    return OpponentRepository.load().assets
