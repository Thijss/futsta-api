from fastapi import APIRouter, Depends

from app.auth import api_key_read_access_auth
from app.repositories.stats import StatRepository
from app.models.goals import CountType

router = APIRouter()


@router.get("/top_assists", dependencies=[Depends(api_key_read_access_auth)])
async def top_assists():
    return StatRepository.from_goals(count_type=CountType.ASSIST).stats


@router.get("/top_goals", dependencies=[Depends(api_key_read_access_auth)])
async def top_goals():
    return StatRepository.from_goals(count_type=CountType.GOAL).stats
