from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .models import (
    RoundSessionModel,
    SolveModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
)

User = get_user_model()


class SolveService:
    def solve_create(self, params, data, user_id):
        user = User.objects.get(id=user_id)
        contest = ContestModel.objects.get(id=params['contest_id'])
        discipline = DisciplineModel.objects.get(id=params['discipline_id'])
        scramble = ScrambleModel.objects.get(id=params['scramble_id'])

        try:
            round_session = RoundSessionModel.objects.get(
                user=user_id,
                discipline=discipline,
                contest=contest,
            )
        except ObjectDoesNotExist:
            round_session = RoundSessionService.round_session_create(
                contest_id=params['contest_id'],
                discipline_id=params['discipline_id'],
                user_id=user_id,
            )

        solve = SolveModel.objects.create(
            time_ms=data.time_ms,
            is_dnf=data.is_dnf,
            reconstruction=data.reconstruction,
            submission_state='pending',

            user=user,
            contest=contest,
            discipline=discipline,
            round_session=round_session,
            scramble=scramble,
        )
        return solve

    def solve_submit(self):
        pass


class RoundSessionService:
    def round_session_create(self, contest_id, discipline_id, user_id):
        contest = ContestModel.objects.get(id=contest_id)
        discipline = DisciplineModel.objects.get(id=discipline_id)
        user = User.objects.get(id=user_id)
        round_session = RoundSessionModel(contest=contest, discipline=discipline, user=user)
        round_session.save()
        return round_session

    def round_session_finish(self):
        pass
