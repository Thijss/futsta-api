from datetime import date

from pydantic import BaseModel, validator

from app.models.opponents import Opponent


class Match(BaseModel):
    match_date: date
    opponent: Opponent
    is_home: bool

    @property
    def is_away(self) -> bool:
        return not self.is_home

    @validator("opponent", pre=True)
    def parse_opponent_name(cls, value):
        if isinstance(value, str):
            return Opponent(name=value)
        return value

    def __str__(self):
        return f"A match on {self.match_date.strftime('%Y-%m-%d')}"

    def __eq__(self, other):
        return other == self.match_date

    def __lt__(self, other):
        return self.match_date < other.match_date

    @classmethod
    def dummy_from_match_date(cls, match_date: date):
        """Create a dummy match for comparison"""
        dummy_opponent = Opponent(name="dummy")
        return cls(match_date=match_date, opponent=dummy_opponent, is_home=True)
