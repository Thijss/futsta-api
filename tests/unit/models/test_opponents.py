"""Unit tests for the Opponent model."""
# pylint: disable=missing-function-docstring

from app.models.opponents import Opponent


def test_opponent_name():
    opponent = Opponent(name="TestOpponent")
    assert opponent.name == "TestOpponent"
