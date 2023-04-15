from app.models.players import Player
from app.repositories.base.repo import JsonRepository


class PlayerRepository(JsonRepository):
    assets: list[Player] = []

    class Config:
        json_file_name = "players.json"
