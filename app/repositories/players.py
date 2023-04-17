from app.models.players import Player
from app.repositories.base.repo import JsonRepository


class PlayerRepository(JsonRepository):
    """Repository for players"""

    assets: list[Player] = []

    class Config:
        """Pydantic configuration"""

        json_file_name = "players.json"
