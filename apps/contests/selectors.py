from django.db.models import Avg

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


class SolveSelector:
    def list(self, filters=None):
        pass

    def retrieve(self, pk):
        # TODO add select_related and prefetch_related
        solve = SolveModel.objects.get(id=pk)
        return solve


class ContestSelector:
    def list(self, filters=None):
        contest_set = ContestModel.objects.all()
        # contest_set = ContestFilter(filters, contest_set).qs
        return contest_set
