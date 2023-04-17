from app.models.opponents import Opponent
from app.repositories.base.repo import JsonRepository


class OpponentRepository(JsonRepository):
    """Repository for opponents"""
    assets: list[Opponent] = []

    class Config:
        """Pydantic configuration"""
        json_file_name = "opponents.json"
