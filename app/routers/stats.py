from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth import AccessLevel, api_key_read_access_auth
from app.models.goals import CountType
from app.repositories.stats import StatRepository
from app.settings.api import get_api_settings

router = APIRouter()


@router.get("/top_assists")
async def top_assists(access_level: Annotated[AccessLevel, Depends(api_key_read_access_auth)]):
    """Get the top assists"""
    settings = get_api_settings()
    if access_level is AccessLevel.READ and settings.hide_spoilers:
        return StatRepository.create_dummy(count_type=CountType.ASSIST).stats
    return StatRepository.from_goals(count_type=CountType.ASSIST).stats


@router.get("/top_goals")
async def top_goals(access_level: Annotated[AccessLevel, Depends(api_key_read_access_auth)]):
    """Get the top goals"""
    settings = get_api_settings()
    if access_level is AccessLevel.READ and settings.hide_spoilers:
        return StatRepository.create_dummy(count_type=CountType.GOAL).stats
    return StatRepository.from_goals(count_type=CountType.GOAL).stats
