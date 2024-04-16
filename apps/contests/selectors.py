from django.db.models import Avg, Min, Max
from django.core.exceptions import ObjectDoesNotExist

from config import SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE, SOLVE_PENDING_STATE
from .models import (
    RoundSessionModel,
    SolveModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
)
from .filters import (
    RoundSessionFilter,
    ContestFilter,
)


class RoundSessionSelector:

    def list_with_solves(self, filters=None):
        filters = filters or {}
        # TODO add prefetch_related & select_related
        round_session_set = RoundSessionModel.objects.all()

        return RoundSessionFilter(filters, round_session_set).qs

    def retrieve_with_solves(self, params, user_id):
        round_session = RoundSessionModel.objects.get(
            user_id=user_id,
            contest_id=params['contest_id'],
            discipline_id=params['discipline_id']
        )
        return round_session

    def retrieve_place(self, params, user_id):
        # Assuming the rating field in the Rating model is named 'value'
        round_session = RoundSessionModel.objects.filter(
            user_id=user_id,
            contest_id=params['contest_id'],
            discipline_id=params['discipline_id']
        ).aggregate(Avg('avg_ms'))['avg_ms__avg']

        higher_rated_round_sessions = RoundSessionModel.objects.filter(
            avg_ms__lt=round_session,
            contest_id=params['contest_id'],
            discipline_id=params['discipline_id']
        )
        print(higher_rated_round_sessions)
        place = higher_rated_round_sessions.count() + 1
        return place

    def retrieve_current(self, params, user_id):
        round_session = RoundSessionModel.objects.get(
            user=user_id, contest__slug=params['contest_slug'],
            discipline_slug=params['discipline_slug'],
            user_id=user_id
        )
        return round_session

    def is_finished(self, discipline_id, contest_id, user_id):
        round_session = RoundSessionModel.objects.get(
            user=user_id, contest__slug=contest_id,
            discipline_id=discipline_id,
            user_id=user_id
        )
        is_finished = round_session.is_finished
        return is_finished


class SolveSelector:
    def list(self, filters=None):
        pass

    def retrieve(self, pk):
        # TODO add select_related and prefetch_related
        solve = SolveModel.objects.get(id=pk)
        return solve

    def list_best_in_every_discipline(self):

        disciplines = DisciplineModel.objects.all()
        solve_set = []
        # TODO add select related and prefetch related
        for discipline in disciplines:
            solve = discipline.solve_set.order_by('time_ms').filter(submission_state='submitted',
                                                                    round_session__is_finished=True,
                                                                    is_dnf=False).first()
            if solve:
                solve_set.append(solve)
        return solve_set

    def list_best_of_every_user(self, params):

        solve_set = SolveModel.objects.annotate(best_time_ms=Min('time_ms'))
        return solve_set

    def onging_contest_submitted(self, contest_slug, discipline_slug, user_id):
        solve_set = SolveModel.objects.filter(
            user=user_id,
            # contest__slug=contest_slug,
            # discipline__slug=discipline_slug,
            # submission_state='submitted',
        )
        return solve_set

    def retrieve_current(self, contest_slug, discipline_slug, user_id):
        try:
            solve = SolveModel.objects.get(
                contest__slug=contest_slug,
                discipline__slug=discipline_slug,
                user=user_id,
                submission_state='pending'
            )
        except ObjectDoesNotExist:
            solve = None
        return solve

    def can_change_current_to_extra(self, contest_slug, discipline_slug, user_id):
        solve_set = SolveModel.objects.filter(
            contest__slug=contest_slug,
            discipline__slug=discipline_slug,
            user=user_id,
            submission_state='changed_to_extra'
        )
        if len(solve_set) >= 2:
            return False
        else:
            return True


class ContestSelector:
    def current_retrieve(self):
        current_contest = ContestModel.objects.filter(is_ongoing=True).last()
        return current_contest

    def list(self, filters=None):
        filters = filters or {}

        contest_set = ContestModel.objects.all()
        return ContestFilter(filters, contest_set).qs


class ScrambleSelector:
    def retrieve_current(self, contest_slug, discipline_slug, user_id):
        scrambles = ContestModel.objects.get(slug=contest_slug).scramble_set.all()
        previous_solve = None
        for scramble in scrambles:
            solve = scramble.solve_set.filter(user=user_id).first()
            if not solve:
                if not previous_solve:
                    return scramble
                elif previous_solve.state == SOLVE_SUBMITTED_STATE:
                    return scramble
                elif previous_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                    while True:
                        extra_scramble = ScrambleModel.objects.get(id=previous_solve.extra_id)
                        extra_solve = extra_scramble.solve_set.filter(user=user_id).first()
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
