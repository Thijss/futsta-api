from datetime import date

from fastapi import APIRouter, Depends
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.models.goals import Goal
from app.repositories.goals.repo import GoalRepository
from app.repositories.goals.validators import validate_involved_players, validate_is_last_goal, \
    validate_subsequent_goal, validate_score
from app.routers._helpers import add_or_raise_http_exception, remove_or_raise_http_exception

router = APIRouter()


@router.get("/{match_date}", dependencies=[Depends(api_key_read_access_auth)])
async def get_by_match_date(match_date: date):
    """Get goals by match date."""
    goals = GoalRepository.load()
    return goals.get_by_match_date(match_date)


@router.post(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_201_CREATED,
)
async def add_goal(goal: Goal):
    """Add a goal."""
    repo = GoalRepository.load()

    validators = [
        validate_involved_players,
        validate_subsequent_goal,
        validate_score,
    ]

    add_or_raise_http_exception(repo, goal, validators)
    return goal


@router.delete("", dependencies=[Depends(api_key_write_access_auth)])
async def remove_goal(goal: Goal):
    """Remove a goal."""
    repo = GoalRepository.load()
    remove_or_raise_http_exception(repo, goal, [validate_is_last_goal])
    return goal
