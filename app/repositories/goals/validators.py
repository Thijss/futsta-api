from app.exceptions import ValidationError
from app.models.goals import Goal, Score
from app.repositories.base.validators import assert_in
from app.repositories.goals.repo import GoalRepository
from app.repositories.matches.repo import MatchRepository
from app.repositories.players import PlayerRepository


def validate_involved_players(goal, *_args):
    """Validate that the players involved in the goal are in the player repository"""
    player_repo = PlayerRepository.load()
    if scoring_player := goal.scored_by:
        assert_in(scoring_player, player_repo)
    if assisting_player := goal.assisted_by:
        assert_in(assisting_player, player_repo)


def validate_subsequent_goal(goal: Goal, repo: GoalRepository):
    """Validate that the goal is the next goal in the match"""
    match_goals = repo.get_by_match_date(goal.match_date)
    if goal.order == 1 and not match_goals:
        return
    if not match_goals:
        raise ValidationError(f"Invalid goal: score {goal.score} cannot be the first score in a match")
    previous_goal = max(match_goals)
    if goal.order != previous_goal.order + 1:
        raise ValidationError(f"Invalid goal: score {goal.score} cannot follow {previous_goal.score}")


def validate_is_last_goal(goal: Goal, repo: GoalRepository):
    """Validate that the goal is the last goal in the match"""
    match_goals = repo.get_by_match_date(goal.match_date)
    if goal.order != len(match_goals):
        raise ValidationError("Not the last goal in the match")


def validate_score(goal: Goal, goal_repo: GoalRepository):
    """Validate that the goal is added to the correct side of the score."""
    match_repo = MatchRepository.load()
    match = match_repo.get_by_match_date(goal.match_date)

    if match.is_home:
        _validate_goal_for_home_match(goal, goal_repo)
    else:
        _validate_goal_for_away_match(goal, goal_repo)


def _validate_goal_for_away_match(goal: Goal, repo: GoalRepository):
    """Validate that the goal is valid for an away match"""
    same_left, same_right = _get_score_changes(goal, repo)
    if same_left and same_right:
        raise ValidationError("Invalid score: team and opponent scores cannot both stay the same")
    if not same_left and not same_right:
        raise ValidationError("Invalid score: team and opponent scores cannot both change")
    if goal.is_team_goal and same_right:
        raise ValidationError("Invalid score: team goal, so team score should increase")
    if goal.is_opponent_goal and same_left:
        raise ValidationError("Invalid score: opponent goal, so opponent score should increase")


def _validate_goal_for_home_match(goal: Goal, repo: GoalRepository):
    """Validate that the goal is valid for a home match"""
    same_left, same_right = _get_score_changes(goal, repo)
    if goal.is_team_goal and same_left:
        raise ValidationError("Invalid score: team goal, so team score should increase")
    if goal.is_opponent_goal and same_right:
        raise ValidationError("Invalid score: opponent goal, so opponent score should increase")


def _get_score_changes(goal: Goal, repo: GoalRepository) -> tuple[bool, bool]:
    match_goals = repo.get_by_match_date(goal.match_date)
    if match_goals:
        previous_score = max(match_goals).score
    else:
        previous_score = Score.construct(home=0, away=0)

    same_left = goal.score.home == previous_score.home
    same_right = goal.score.away == previous_score.away

    return same_left, same_right
