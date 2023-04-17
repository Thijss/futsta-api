from app.models.opponents import Opponent


def test_opponent_name():
    opponent = Opponent(name="TestOpponent")
    assert opponent.name == "TestOpponent"
