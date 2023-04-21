# pylint: disable=missing-function-docstring
from datetime import date, datetime

import pytest

from app.exceptions import NotFoundError
from app.repositories.matches.repo import MatchRepository


def test_match_repository_get_by_match_date(home_match):
    match_repo = MatchRepository()

    match_repo.assets = [home_match]

    # test get by match date with valid data
    match = match_repo.get_by_match_date(datetime.now().date())
    assert match.match_date == datetime.now().date()

    # test get by match date with invalid data
    with pytest.raises(NotFoundError):
        match_repo.get_by_match_date(date(2023, 4, 19))

    match_repo.assets = [match, match]
    with pytest.raises(AssertionError):
        match_repo.get_by_match_date(datetime.now().date())
