from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.exceptions import AlreadyExistsError
from app.models.opponents import Opponent
from app.repositories.base.validators import assert_not_in
from app.repositories.opponents import OpponentRepository

router = APIRouter()


@router.post("", dependencies=[Depends(api_key_write_access_auth)], status_code=status.HTTP_201_CREATED)
async def add_opponent(opponent: Opponent):
    repo = OpponentRepository.load()
    try:
        repo.add(asset=opponent, validators=[assert_not_in])
    except AlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    return opponent


@router.get("", dependencies=[Depends(api_key_read_access_auth)])
async def list_opponents():
    return OpponentRepository.load().assets
