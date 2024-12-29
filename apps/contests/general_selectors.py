from django.core.exceptions import ObjectDoesNotExist

from config import SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE, SOLVE_PENDING_STATE
from .models import (
    ContestModel,
    ScrambleModel,
    SolveModel,
    TnoodleScramblesModel
)


def current_contest_retrieve():
    try:
        current_contest = ContestModel.objects.filter(is_ongoing=True).last()
        return current_contest
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist()


def retrieve_current_scramble(contest, user):
    scrambles = contest.scramble_set.all()
    previous_solve = None
    for scramble in scrambles:
        solve = scramble.solve_set.filter(user=user).first()
        if not solve:
            if not previous_solve:
                return scramble
            elif previous_solve.state == SOLVE_SUBMITTED_STATE:
                return scramble
            elif previous_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                while True:
                    extra_scramble = ScrambleModel.objects.get(id=previous_solve.extra_id)
                    extra_solve = extra_scramble.solve_set.filter(user=user).first()
                    if not extra_solve:
                        return extra_scramble
                    elif extra_solve.state == SOLVE_PENDING_STATE:
                        return extra_scramble
                    elif extra_solve.state == SOLVE_SUBMITTED_STATE:
                        return scramble
                    elif extra_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                        previous_solve = extra_solve

        elif solve.submission_state == SOLVE_PENDING_STATE:
            return scramble
        else:
            pass


def retrieve_current_scramble_avg5(contest, discipline, user):
    # check if round_session exists
    try:
        round_session = contest.round_session_set.get(user=user)
    except ObjectDoesNotExist:
        current_scramble_position = '1'
        current_scramble = contest.scramble_set.get(position=current_scramble_position, discipline=discipline)
        return current_scramble

    # check if round_session is not finished
    if round_session.is_finished:
        return None

    # case if solve is pending
    last_solve = round_session.solve_set.last()
    if last_solve.submission_state == 'pending':
        current_scramble = last_solve.scramble
        return current_scramble

    # find all available scramble positions
    available_scramble_positions = ['1', '2', '3', '4', '5',]
    available_extra_scramble_positions = ['E1', 'E2']
    for solve in round_session.solve_set.all():
        if solve.scramble.position in available_scramble_positions:
            available_scramble_positions.remove(solve.scramble.position)
        if solve.scramble.position in available_extra_scramble_positions:
            available_extra_scramble_positions.remove(solve.scramble.position)

    # case if solve is submitted
    if last_solve.submission_state == 'submitted':
        current_scramble = contest.scramble_set.get(position=available_scramble_positions[0], discipline=discipline)
        return current_scramble

    # case if solve is changed_to_extra
    if last_solve.submission_state == 'changed_to_extra':
        current_scramble = contest.scramble_set.get(position=available_extra_scramble_positions[0], discipline=discipline)
        return current_scramble


def can_change_solve_to_extra(contest, discipline, user):
    solve_set = SolveModel.objects.filter(
        contest=contest,
        discipline=discipline,
        user=user,
        submission_state='changed_to_extra'
    )
    if len(solve_set) >= 2:
        return False
    else:
        return True
