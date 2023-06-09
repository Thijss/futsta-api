"""Unit tests for the goals repository."""
# pylint: disable=missing-function-docstring

from datetime import datetime
from unittest.mock import patch

import pytest

from app.exceptions import ValidationError
from app.models.goals import Goal, Score
from app.models.players import Player
from app.repositories.goals import validators
from app.repositories.goals.validators import (
    validate_involved_players,
    validate_is_last_goal,
    validate_score,
    validate_subsequent_goal,
)
from app.repositories.matches.repo import MatchRepository
from app.repositories.players import PlayerRepository


def test_validate_score_for_away_match_raises_error_both_change(away_repo, away_match):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by="Thijs",
        assisted_by=None,
        score=Score(home=1, away=1),
    )

    match_repo = MatchRepository()
    match_repo.assets = [away_match]

    with patch.object(validators.MatchRepository, "load", return_value=match_repo):
        with pytest.raises(ValidationError) as error:
            validate_score(next_goal, away_repo)
    assert "team and opponent scores cannot both change" in str(error.value)


def test_validate_score_for_away_match_raises_error_wrong_side(away_repo, away_match):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by="Thijs",
        assisted_by=None,
        score=Score(home=1, away=2),
    )

    match_repo = MatchRepository()
    match_repo.assets = [away_match]

    with patch.object(validators.MatchRepository, "load", return_value=match_repo):
        with pytest.raises(ValidationError) as error:
            validate_score(next_goal, away_repo)
    assert "team goal, so team score should increase" in str(error.value)


def test_validate_score_for_away_match_raises_error_same_score(away_repo, away_match):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by="Thijs",
        assisted_by=None,
        score=Score(home=0, away=2),
    )
    match_repo = MatchRepository()
    match_repo.assets = [away_match]

    with patch.object(validators.MatchRepository, "load", return_value=match_repo):
        with pytest.raises(ValidationError) as error:
            validate_score(next_goal, away_repo)
    assert "team and opponent scores cannot both stay the same" in str(error.value)


def test_validate_score_for_away_match_does_not_raise_error(away_repo, away_match):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by="Thijs",
        assisted_by=None,
        score=Score(home=0, away=3),
    )
    match_repo = MatchRepository()
    match_repo.assets = [away_match]

    with patch.object(validators.MatchRepository, "load", return_value=match_repo):
        validate_score(next_goal, away_repo)


def test_validate_score_for_home_match_raises_error(home_repo, home_match):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by="Thijs",
        assisted_by=None,
        score=Score(home=1, away=1),
    )

    match_repo = MatchRepository()
    match_repo.assets = [home_match]

    with patch.object(validators.MatchRepository, "load", return_value=match_repo):
        with pytest.raises(ValidationError) as error:
            validate_score(next_goal, home_repo)
    assert "team goal, so team score should increase" in str(error.value)


def test_validate_score_for_home_match_does_not_raise_error(home_repo, home_match):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by=None,
        assisted_by=None,
        score=Score(home=1, away=1),
    )
    match_repo = MatchRepository()
    match_repo.assets = [home_match]

    with patch.object(validators.MatchRepository, "load", return_value=match_repo):
        validate_score(next_goal, home_repo)


def test_validate_subsequent_goal_raises_error(home_repo):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by=None,
        assisted_by=None,
        score=Score(home=4, away=1),
    )
    with pytest.raises(ValidationError):
        validate_subsequent_goal(next_goal, home_repo)


def test_validate_subsequent_goal_does_not_raise_error(home_repo):
    next_goal = Goal(
        match_date=datetime.now().date(),
        scored_by=None,
        assisted_by=None,
        score=Score(home=2, away=0),
    )
    validate_subsequent_goal(next_goal, home_repo)


def test_validate_is_last_goal_raises_error(away_repo):
    last_goal = Goal(
        match_date=datetime.now().date(),
        scored_by=None,
        assisted_by=None,
        score=Score(home=0, away=1),
    )
    with pytest.raises(ValidationError):
        validate_is_last_goal(last_goal, away_repo)


def test_validate_is_last_goal_does_not_raise_error(away_repo):
    last_goal = Goal(
        match_date=datetime.now().date(),
        scored_by=None,
        assisted_by=None,
        score=Score(home=0, away=2),
    )
    validate_is_last_goal(last_goal, away_repo)


def test_validate_involved_players_raises_error():
    goal = Goal(
        match_date=datetime.now().date(),
        scored_by="John",
        assisted_by=None,
        score=Score(home=2, away=0),
    )

    player_1 = Player(name="Bill")

    player_repo = PlayerRepository()
    player_repo.assets = [player_1]

    with patch.object(validators.PlayerRepository, "load", return_value=player_repo):
        with pytest.raises(ValidationError) as error:
            validate_involved_players(goal)

    assert "A player named John does not exist" in str(error.value)


def test_validate_involved_players_does_not_raises_error():
    goal = Goal(
        match_date=datetime.now().date(),
        scored_by="John",
        assisted_by=None,
        score=Score(home=2, away=0),
    )

    player_1 = Player(name="John")

    player_repo = PlayerRepository()
    player_repo.assets = [player_1]

    with patch.object(validators.PlayerRepository, "load", return_value=player_repo):
        validate_involved_players(goal)
