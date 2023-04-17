from collections import Counter
from datetime import date

from app.exceptions import ValidationError
from app.models.goals import CountType, Goal, Score
from app.models.matches import Match
from app.repositories.base.repo import JsonRepository


class GoalRepository(JsonRepository):
    assets: list[Goal] = []

    class Config:
        json_file_name = "goals.json"

    def get_next_score(self, goal: Goal, match: Match) -> Score:
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
        return [goal for goal in self.assets if goal.match_date == match_date]

    def get_player_counts(self, count_type: CountType) -> Counter:
        if count_type is CountType.GOAL:
            attr = "scored_by"
        elif count_type is CountType.ASSIST:
            attr = "assisted_by"
        else:
            raise NotImplementedError(f"Invalid count_type {CountType}")

        counter = Counter([getattr(goal, attr) for goal in self.assets])
        counter.pop(None)
        return counter


def validate_goal_for_away_match(repo: GoalRepository, goal: Goal):
    same_left, same_right = _get_score_changes(repo, goal)
    if same_left and same_right:
        raise ValidationError("Invalid score: team and opponent scores cannot both stay the same")
    if not same_left and not same_right:
        raise ValidationError("Invalid score: team and opponent scores cannot both change")
    if goal.is_team_goal and same_right:
        raise ValidationError("Invalid score: team goal, so team score should increase")
    if goal.is_opponent_goal and same_left:
        raise ValidationError("Invalid score: opponent goal, so opponent score should increase")


def validate_goal_for_home_match(repo: GoalRepository, goal: Goal):
    same_left, same_right = _get_score_changes(repo, goal)
    if goal.is_team_goal and same_left:
        raise ValidationError("Invalid score: team goal, so team score should increase")
    if goal.is_opponent_goal and same_right:
        raise ValidationError("Invalid score: opponent goal, so opponent score should increase")


def validate_subsequent_goal(repo: GoalRepository, goal: Goal):
    match_goals = repo.get_by_match_date(goal.match_date)
    if goal.order == 1 and not match_goals:
        return
    if not match_goals:
        raise ValidationError(f"Invalid goal: score {goal.score} cannot be the first score in a match")
    previous_goal = max(match_goals)
    if goal.order != previous_goal.order + 1:
        raise ValidationError(f"Invalid goal: score {goal.score} cannot follow {previous_goal.score}")


def validate_is_last_goal(repo: GoalRepository, goal: Goal):
    match_goals = repo.get_by_match_date(goal.match_date)
    if goal.order != len(match_goals):
        raise ValidationError("Not the last goal in the match")


def _get_score_changes(repository: GoalRepository, goal: Goal) -> tuple[bool, bool]:
    match_goals = repository.get_by_match_date(goal.match_date)
    if match_goals:
        previous_score = max(match_goals).score
    else:
        previous_score = Score.construct(home=0, away=0)

    same_left = goal.score.home == previous_score.home
    same_right = goal.score.away == previous_score.away

    return same_left, same_right
