from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.exceptions import AlreadyExistsError
from app.models.players import Player
from app.repositories.base.validators import assert_not_in
from app.repositories.players import PlayerRepository

router = APIRouter()


@router.post(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_201_CREATED,
)
async def add_player(player: Player):
    """Add a player."""
    repo = PlayerRepository.load()
    try:
        repo.add(player, validators=[assert_not_in])
    except AlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return player


@router.get("", dependencies=[Depends(api_key_read_access_auth)])
async def list_players():
    """List all players."""
    players = PlayerRepository.load().assets
    return sorted(players, key=lambda player: player.name)
