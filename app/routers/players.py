from fastapi import APIRouter, Depends
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.models.players import Player
from app.repositories.base.validators import assert_not_in
from app.repositories.players import PlayerRepository
from app.routers._helpers import add_or_raise_http_exception

router = APIRouter()


@router.post(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_201_CREATED,
)
async def add_player(player: Player):
    """Add a player."""
    repo = PlayerRepository.load()
    add_or_raise_http_exception(repo, player, [assert_not_in])
    return player


@router.get("", dependencies=[Depends(api_key_read_access_auth)])
async def list_players():
    """List all players."""
    players = PlayerRepository.load().assets
    return sorted(players, key=lambda player: player.name)
