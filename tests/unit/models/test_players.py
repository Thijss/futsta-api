from app.models.players import Player


def test_create_player():
    name = "TestPlayer"
    player = Player(name=name)
    assert player.name == name


def test_create_player_from_integer():
    name = 123
    player = Player(name=name)
    assert player.name == "123"


def test_player_hashing():
    name = "TestPlayer"
    player = Player(name=name)
    assert hash(player) == hash(name)


def test_player_equality():
    name1 = "TestPlayer1"
    name2 = "TestPlayer2"
    player1 = Player(name=name1)
    player2 = Player(name=name2)
    player3 = Player(name=name1)
    assert player1 == player3
    assert player1 != player2


def test_player_string_representation():
    name = "TestPlayer"
    player = Player(name=name)
    assert str(player) == "A player named TestPlayer"
