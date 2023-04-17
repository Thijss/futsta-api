from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from app.models.players import Player
from app.utils import int_to_ordinal


class CountType(str, Enum):
    """The type of count"""
    ASSIST = "assist"
    GOAL = "goal"


# noinspection PyMethodParameters
class Score(BaseModel):
    """A score"""
    home: int
    away: int

    @property
    def order(self) -> int:
        """Return the order of the score in the match"""
        return self.home + self.away

    @classmethod
    @validator("away")
    def validate_score(cls, value, values):
        """Validate the score"""
        if value == 0 and values.get("home") == 0:
            raise ValueError("Invalid score '0-0'")
        return value

    def __str__(self):
        return f"{self.home}-{self.away}"


class Goal(BaseModel):
    """A goal scored in a match"""
    match_date: date
    scored_by: Optional[Player] = None
    assisted_by: Optional[Player] = None
    score: Optional[Score] = None

    @property
    def order(self) -> int:
        """Return the order of the goal in the match"""
        return self.score.order

    @property
    def is_team_goal(self) -> bool:
        """Return True if the goal was scored by the team"""
        return self.scored_by is not None

    @property
    def is_opponent_goal(self) -> bool:
        """Return True if the goal was scored by the opponent team"""
        return not self.is_team_goal

    def dict(self, *args, **kwargs):
        """Return a dictionary representation of the goal"""
        serialized = super().dict(*args, **kwargs)
        serialized["is_team_goal"] = self.is_team_goal
        serialized["order"] = self.order
        return serialized

    @classmethod
    @validator("scored_by", "assisted_by", pre=True)
    def parse_player_name(cls, value):
        """Parse a player name from a string or a Player object"""
        if isinstance(value, str):
            return Player(name=value)
        return value

    @classmethod
    @validator("score", pre=True)
    def parse_score(cls, value):
        """Parse a score from a string or a Score object"""
        if isinstance(value, str):
            home, away = value.split("-")
            return Score(home=home, away=away)
        return value

    @classmethod
    @validator("assisted_by")
    def validate_assisted_by(cls, value, values):
        """Validate that an assist is only given if there is a goal scorer"""
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
        """Pydantic configuration"""
        schema_extra = {
            "example": {
                "match_date": datetime.now().strftime("%Y-%m-%d"),
                "scored_by": "Thijs",
                "assisted_by": "Mark",
            }
        }
