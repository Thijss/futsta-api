from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from app.models.players import Player
from app.utils import int_to_ordinal


class CountType(str, Enum):
    ASSIST = "assist"
    GOAL = "goal"


# noinspection PyMethodParameters
class Score(BaseModel):
    home: int
    away: int

    @property
    def order(self) -> int:
        return self.home + self.away

    @validator("away")
    def validate_score(cls, value, values):
        if value == 0 and values.get("home") == 0:
            raise ValueError("Invalid score '0-0'")
        return value

    def __str__(self):
        return f"{self.home}-{self.away}"


class Goal(BaseModel):
    match_date: date
    scored_by: Optional[Player] = None
    assisted_by: Optional[Player] = None
    score: Optional[Score] = None

    @property
    def order(self) -> int:
        return self.score.order

    @property
    def is_team_goal(self) -> bool:
        return self.scored_by is not None

    @property
    def is_opponent_goal(self) -> bool:
        return not self.is_team_goal

    def dict(self, *args, **kwargs):
        serialized = super().dict(*args, **kwargs)
        serialized["is_team_goal"] = self.is_team_goal
        serialized["order"] = self.order
        return serialized

    @classmethod
    @validator("scored_by", "assisted_by", pre=True)
    def parse_player_name(cls, value):
        if isinstance(value, str):
            return Player(name=value)
        return value

    @classmethod
    @validator("score", pre=True)
    def parse_score(cls, value):
        if isinstance(value, str):
            return Score(*value.split("-"))
        return value

    @classmethod
    @validator("assisted_by")
    def validate_assisted_by(cls, value, values):
        if value and not values.get("scored_by"):
            raise ValueError("Cannot have an assist without a goal scorer")
        return value

    def __eq__(self, other):
        same_match = other.match_date == self.match_date
        same_order = other.order == self.order
        return same_match and same_order

    def __lt__(self, other: "Goal") -> bool:
        return self.order < other.order

    def __str__(self):
        return f"{int_to_ordinal(self.order)} goal on {self.match_date.strftime('%d-%m-%Y')}"

    class Config:
        schema_extra = {
            "example": {
                "match_date": datetime.now().strftime("%Y-%m-%d"),
                "scored_by": "Thijs",
                "assisted_by": "Mark",
            }
        }
