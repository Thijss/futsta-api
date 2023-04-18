from collections import Counter
from datetime import date

from app.models.goals import CountType, Goal, Score
from app.models.matches import Match
from app.repositories.base.repo import JsonRepository


class GoalRepository(JsonRepository):
    """Repository for goals"""

    assets: list[Goal] = []

    class Config:
        """Pydantic configuration"""

        json_file_name = "goals.json"

    def get_next_score(self, goal: Goal, match: Match) -> Score:
        """Return the score after the goal is scored"""
        match_goals = self.get_by_match_date(goal.match_date)
        if match_goals:
            previous_score = max(match_goals).score
        else:
            previous_score = Score.construct(home=0, away=0)

        home_match_team_goal = match.is_home and goal.is_team_goal
        home_match_opponent_goal = match.is_home and goal.is_opponent_goal
        away_match_team_goal = match.is_away and goal.is_team_goal
        away_match_opponent_goal = match.is_away and goal.is_opponent_goal

        next_score = previous_score.copy()
        if home_match_team_goal or away_match_opponent_goal:
            next_score.home += 1

        if home_match_opponent_goal or away_match_team_goal:
            next_score.away += 1

        return next_score

    def get_by_match_date(self, match_date: date) -> list[Goal]:
        """Return a list of goals scored in a match"""
        return [goal for goal in self.assets if goal.match_date == match_date]

    def get_player_counts(self, count_type: CountType) -> Counter:
        """Return a counter of the number of goals or assists scored by each player"""
        if count_type is CountType.GOAL:
            attr = "scored_by"
        elif count_type is CountType.ASSIST:
            attr = "assisted_by"
        else:
            raise NotImplementedError(f"Invalid count_type {CountType}")

        counter = Counter([getattr(goal, attr) for goal in self.assets])
        counter.pop(None)
        return counter
