from datetime import date, datetime

import pytest

from app.models.goals import Goal, Score
from app.models.matches import Match
from app.models.opponents import Opponent
from app.repositories.goals.repo import GoalRepository


@pytest.fixture(name="home_goal")
def home_goal_fixture():
    """Fixture for a home goal"""
    return Goal(
        match_date=datetime.now().date(),
        scored_by="Thijs",
        assisted_by="Mark",
        score=Score(home=1, away=0),
    )


@pytest.fixture(name="away_goal")
def away_goal_fixture():
    """Fixture for an away goal"""
    return Goal(
        match_date=datetime.now().date(),
        scored_by="Thijs",
        assisted_by="Mark",
        score=Score(home=0, away=1),
    )


@pytest.fixture(name="home_repo")
def home_repo_fixture(home_goal):
    """Fixture for a repository with one home goal"""
    repo = GoalRepository()
    repo.assets = [home_goal]
    return repo


@pytest.fixture(name="away_repo")
def away_repo_fixture(away_goal):
    """Fixture for a repository with two away goals"""
    repo = GoalRepository()
    another_goal = Goal(
        match_date=datetime.now().date(),
        scored_by="Mark",
        assisted_by="Thijs",
        score=Score(home=0, away=2),
    )
    repo.assets = [away_goal, another_goal]
    return repo


@pytest.fixture(name="away_match")
def away_match_fixture():
    """Fixture for an away match"""
    return Match(match_date=date(2023, 4, 18), opponent=Opponent(name="TestOpponent"), is_home=False)


@pytest.fixture(name="home_match")
def home_match_fixture():
    """Fixture for a home match"""
    return Match(match_date=date(2023, 4, 18), opponent=Opponent(name="TestOpponent"), is_home=True)
