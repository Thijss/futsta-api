from datetime import date

from app.exceptions import NotFoundError
from app.models.matches import Match
from app.repositories.base.repo import JsonRepository


class MatchRepository(JsonRepository):
    assets: list[Match] = []

    class Config:
        json_file_name = "matches.json"

    def get_by_match_date(self, match_date: date) -> Match:
        if match_list := [match for match in self.assets if match.match_date == match_date]:
            assert len(match_list) == 1, f"Multiple matches found for {match_date}"
            return match_list[0]
        raise NotFoundError(f"No match found for {match_date}")
