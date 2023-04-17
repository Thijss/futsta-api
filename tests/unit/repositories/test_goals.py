"""Unit tests for the goals repository."""
# pylint: disable=missing-function-docstring

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.exceptions import ValidationError
from app.models.goals import Goal, Score
from app.repositories.goals import (
    validate_goal_for_away_match,
    validate_goal_for_home_match,
    validate_is_last_goal,
    validate_subsequent_goal,
)


@pytest.fixture(name="home_goal")
def home_goal_fixture():
    return Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by="Mark", score=Score(home=1, away=0))


@pytest.fixture(name="away_goal")
def away_goal_fixture():
    return Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by="Mark", score=Score(home=0, away=1))


@pytest.fixture(name="home_repo")
def home_repo_fixture(home_goal):
    repo = MagicMock()
    repo.goals = [home_goal]
    repo.get_by_match_date.return_value = [goal for goal in repo.goals if goal.match_date == datetime.now().date()]
    return repo


@pytest.fixture(name="away_repo")
def away_repo_fixture(away_goal):
    repo = MagicMock()
    another_goal = Goal(
        match_date=datetime.now().date(), scored_by="Mark", assisted_by="Thijs", score=Score(home=0, away=2)
    )
    repo.goals = [away_goal, another_goal]
    repo.get_by_match_date.return_value = [goal for goal in repo.goals if goal.match_date == datetime.now().date()]
    return repo


def test_validate_goal_for_away_match_raises_error(away_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by=None, score=Score(home=1, away=1))
    with pytest.raises(ValidationError):
        validate_goal_for_away_match(away_repo, next_goal)


def test_validate_goal_for_away_match_raises_error_v2(away_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by=None, score=Score(home=1, away=2))
    with pytest.raises(ValidationError):
        validate_goal_for_away_match(away_repo, next_goal)


def test_validate_goal_for_away_match_raises_error_v3(away_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by=None, score=Score(home=0, away=2))
    with pytest.raises(ValidationError):
        validate_goal_for_away_match(away_repo, next_goal)


def test_validate_goal_for_away_match_does_not_raise_error(away_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by=None, score=Score(home=0, away=3))
    validate_goal_for_away_match(away_repo, next_goal)


def test_validate_goal_for_home_match_raises_error(home_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by=None, score=Score(home=1, away=1))

    with pytest.raises(ValidationError):
        validate_goal_for_home_match(home_repo, next_goal)


def test_validate_goal_for_home_match_does_not_raise_error(home_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by=None, assisted_by=None, score=Score(home=1, away=1))
    validate_goal_for_home_match(home_repo, next_goal)


def test_validate_subsequent_goal_raises_error(home_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by=None, assisted_by=None, score=Score(home=4, away=1))
    with pytest.raises(ValidationError):
        validate_subsequent_goal(home_repo, next_goal)


def test_validate_subsequent_goal_does_not_raise_error(home_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by=None, assisted_by=None, score=Score(home=2, away=0))
    validate_subsequent_goal(home_repo, next_goal)


def test_validate_is_last_goal_raises_error(away_repo):
    next_goal = Goal(match_date=datetime.now().date(), scored_by=None, assisted_by=None, score=Score(home=0, away=1))
    with pytest.raises(ValidationError):
        validate_is_last_goal(away_repo, next_goal)


def test_validate_is_last_goal_does_not_raise_error(away_repo):
    last_goal = Goal(match_date=datetime.now().date(), scored_by=None, assisted_by=None, score=Score(home=0, away=2))
    validate_is_last_goal(away_repo, last_goal)
