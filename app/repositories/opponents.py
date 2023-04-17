from app.models.opponents import Opponent
from app.repositories.base.repo import JsonRepository


class OpponentRepository(JsonRepository):
    assets: list[Opponent] = []

    class Config:
        json_file_name = "opponents.json"
