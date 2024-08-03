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

def retrieve_current_scramble_by_round_session(contest, user):
    try:
        round_session = contest.objects.round_session_set.get(user=user)
    except ObjectDoesNotExist:
        round_session = None
        # send first scramble back

    # check if round_session is completed

    # check if round_session


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
