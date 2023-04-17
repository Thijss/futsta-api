import pytest
from datetime import datetime
from app.models.goals import Goal, Score


@pytest.fixture
def goal():
    return Goal(match_date=datetime.now().date(), scored_by="Thijs", assisted_by="Mark", score=Score(home=1, away=0))


def test_goal_properties(goal):
    assert goal.is_team_goal == True
    assert goal.is_opponent_goal == False
    assert goal.order == 1
    assert str(goal) == "1st goal on " + datetime.now().strftime("%d-%m-%Y")


def test_goal_equality(goal):
    assert goal == Goal(
        match_date=datetime.now().date(), scored_by="Thijs", assisted_by="Mark", score=Score(home=1, away=0)
    )


def test_goal_inequality(goal):
    assert goal != Goal(
        match_date=datetime.now().date(), scored_by="John", assisted_by=None, score=Score(home=2, away=0)
    )


def test_goal_invalid_assist(goal):
    with pytest.raises(ValueError):
        Goal(match_date=datetime.now().date(), scored_by=None, assisted_by="Thijs", score=Score(home=1, away=0))


def test_goal_invalid_score():
    with pytest.raises(ValueError):
        Score(away=0, home=0)
