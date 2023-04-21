import random
from typing import Union

from pydantic import BaseModel

from app.models.goals import CountType
from app.models.players import Player
from app.repositories.goals.repo import GoalRepository
from app.repositories.players import PlayerRepository


class _GoalStat(BaseModel):
    player: Player
    count: int


class _AssistStat(BaseModel):
    player: Player
    count: int


class StatRepository(BaseModel):
    """A repository of stats"""

    stats: list[Union[_GoalStat, _AssistStat]]

    @classmethod
    def from_goals(cls, count_type: CountType):
        """Create a repository of stats from goals"""
        goals = GoalRepository.load()
        players = PlayerRepository.load().assets
        player_counts = goals.get_player_counts(count_type)

        for player in players:
            if player not in player_counts:
                player_counts[player] = 0

        counter_class = cls.get_counter_class(count_type)
        repo = cls(stats=[counter_class(player=player, count=count) for player, count in player_counts.items()])
        repo.stats = sorted(repo.stats, key=lambda stat: stat.count, reverse=True)
        return repo

    @classmethod
    def create_dummy(cls, count_type: CountType):
        """Create a dummy repository of stats"""
        counter_class = cls.get_counter_class(count_type)

        players = PlayerRepository.load().assets

        stats = [counter_class(player=player, count=-1) for player in players]
        random.shuffle(stats)
        repo = cls(stats=stats)
        return repo

    @staticmethod
    def get_counter_class(count_type: CountType):
        """Return the counter class for the given count type"""
        if count_type is CountType.GOAL:
            return _GoalStat
        if count_type is CountType.ASSIST:
            return _AssistStat
        raise NotImplementedError(f"count_type {count_type} is not supported")
