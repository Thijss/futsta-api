from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.exceptions import NotFoundError, ValidationError
from app.models.goals import Goal
from app.repositories.base.validators import assert_in, assert_not_in
from app.repositories.goals import (
    GoalRepository,
    validate_goal_for_away_match,
    validate_goal_for_home_match,
    validate_is_last_goal,
    validate_subsequent_goal,
)
from app.repositories.matches import MatchRepository
from app.repositories.players import PlayerRepository

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
    player_repo = PlayerRepository.load()
    match_repo = MatchRepository.load()
    goal_repo = GoalRepository.load()
    try:
        match = match_repo.get_by_match_date(goal.match_date)
        if scoring_player := goal.scored_by:
            assert_in(player_repo, scoring_player)
        if assisting_player := goal.assisted_by:
            assert_in(player_repo, assisting_player)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"msg": str(error)}]) from error

    if goal.score is None:
        goal.score = goal_repo.get_next_score(goal, match)

    validators = [assert_not_in, validate_subsequent_goal]
    if match.is_home:
        validators.append(validate_goal_for_home_match)
    else:
        validators.append(validate_goal_for_away_match)

    try:
        goal_repo.add(goal, validators=validators)
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{"msg": str(error)}]) from error
    return goal


@router.delete("", dependencies=[Depends(api_key_write_access_auth)])
async def remove_goal(goal: Goal):
    """Remove a goal."""
    try:
        GoalRepository.load().remove(goal, validators=[validate_is_last_goal])
    except ValidationError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return goal
