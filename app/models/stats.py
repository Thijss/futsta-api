from typing import Union

from pydantic import BaseModel

from app.models.goals import CountType
from app.repositories.goals import GoalRepository
from app.models.players import Player
from app.repositories.players import PlayerRepository


class _GoalStat(BaseModel):
    player: Player
    count: int


class _AssistStat(BaseModel):
    player: Player
    count: int


class StatRepository(BaseModel):
    stats: list[Union[_GoalStat, _AssistStat]]

    @classmethod
    def from_goals(cls, count_type: CountType):
        goals = GoalRepository.load()
        players = PlayerRepository.load().assets
        player_counts = goals.get_player_counts(count_type)

        for player in players:
            if player not in player_counts:
                player_counts[player] = 0

        counter_class = cls.get_counter_class(count_type)
        repo = cls(
            stats=[
                counter_class(player=player, count=count)
                for player, count in player_counts.items()
            ]
        )
        repo.stats = sorted(repo.stats, key=lambda stat: stat.count, reverse=True)
        return repo

    @staticmethod
    def get_counter_class(count_type: CountType):
        if count_type is CountType.GOAL:
            return _GoalStat
        if count_type is CountType.ASSIST:
            return _AssistStat
        raise NotImplementedError(f"count_type {count_type} is not supported")
