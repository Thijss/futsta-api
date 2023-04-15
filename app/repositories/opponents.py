from app.models.opponents import Opponent
from app.repositories.base.repo import JsonRepository


class OpponentRepository(JsonRepository):
    assets: list[Opponent] = []

    @classmethod
    def add(cls, opponent: Opponent):
        repository = cls.load()
        repository.assert_not_in(opponent)
        repository.assets.append(opponent)
        repository.save()

    class Config:
        json_file_name = "opponents.json"
