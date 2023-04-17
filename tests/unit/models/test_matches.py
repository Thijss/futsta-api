from datetime import date
from pytest import raises
from app.models.matches import Match
from app.models.opponents import Opponent


def test_create_match():
    match_date = date(2023, 4, 17)
    opponent = Opponent(name="TestOpponent")
    is_home = True
    match = Match(match_date=match_date, opponent=opponent, is_home=is_home)
    assert match.match_date == match_date
    assert match.opponent == opponent
    assert match.is_home == is_home
    assert match.is_away == (not is_home)


def test_create_match_with_invalid_date():
    match_date = "invalid-date"
    opponent = Opponent(name="TestOpponent")
    is_home = True
    with raises(ValueError):
        Match(match_date=match_date, opponent=opponent, is_home=is_home)


def test_create_match_with_opponent():
    match_date = date(2023, 4, 17)
    opponent = Opponent(name="TestOpponent")
    is_home = True
    match = Match(match_date=match_date, opponent=opponent.name, is_home=is_home)
    assert match.opponent == opponent


def test_match_to_string():
    match_date = date(2023, 4, 17)
    opponent = Opponent(name="TestOpponent")
    is_home = True
    match = Match(match_date=match_date, opponent=opponent, is_home=is_home)
    assert str(match) == "A match on 2023-04-17"


def test_match_equality():
    match_date1 = date(2023, 4, 17)
    match_date2 = date(2023, 4, 18)
    opponent = Opponent(name="TestOpponent")
    is_home = True
    match1 = Match(match_date=match_date1, opponent=opponent, is_home=is_home)
    match2 = Match(match_date=match_date2, opponent=opponent, is_home=is_home)
    assert match1 == match1
    assert match2 == match2
    assert match1 != match2
    assert match2 != match1


def test_match_comparison():
    match_date1 = date(2023, 4, 17)
    match_date2 = date(2023, 4, 18)
    opponent = Opponent(name="TestOpponent")
    is_home = True
    match1 = Match(match_date=match_date1, opponent=opponent, is_home=is_home)
    match2 = Match(match_date=match_date2, opponent=opponent, is_home=is_home)
    assert match1 < match2
    assert match2 > match1


def test_dummy_match():
    match_date = date(2023, 4, 17)
    dummy_match = Match.dummy_from_match_date(match_date)
    assert dummy_match.match_date == match_date
    assert dummy_match.opponent.name == "dummy"
    assert dummy_match.is_home == True
