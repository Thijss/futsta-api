from app.models.matches import Match
from app.repositories.base.validators import assert_in
from app.repositories.opponents import OpponentRepository


def validate_opponent_exists(match: Match, *_args):
    """Validate that the opponent exists in the opponent repository"""
    opponent_repo = OpponentRepository.load()
    assert_in(match.opponent, opponent_repo)
