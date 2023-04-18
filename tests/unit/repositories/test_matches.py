# pylint: disable=missing-function-docstring
from datetime import date

import pytest

from app.exceptions import NotFoundError
from app.models.matches import Match
from app.models.opponents import Opponent
from app.repositories.matches import MatchRepository


@pytest.fixture(name="match")
def match_fixture():
    return Match(match_date=date(2023, 4, 18), opponent=Opponent(name="TestOpponent"), is_home=True)


def test_match_repository_get_by_match_date(match):
    match_repo = MatchRepository()

    match_repo.assets = [match]

    # test get by match date with valid data
    match = match_repo.get_by_match_date(date(2023, 4, 18))
    assert match.match_date == date(2023, 4, 18)

    # test get by match date with invalid data
    with pytest.raises(NotFoundError):
        match_repo.get_by_match_date(date(2023, 4, 19))

    match_repo.assets = [match, match]
    with pytest.raises(AssertionError):
        match_repo.get_by_match_date(date(2023, 4, 18))
