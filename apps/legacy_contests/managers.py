from django.db.transaction import atomic
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist

from config import SOLVE_PENDING_STATE, SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE
from .models import ScrambleModel, SolveModel, ContestModel, DisciplineModel, RoundSessionModel
from apps.accounts.models import User
from scripts.cube import SolveValidator

SOLVES_IN_CONTEST = 5

'''
all cases

1. no previous solve, send first scramble
2. current solve is pending, return current solve and scramble
3. previous solve is submitted, return current solve and scramble
4. previous solve is changed_to_extra, search for extra by id (in change to extra field). If extra is submitted go ahead
'''


class SolveManager:
    def __init__(self, request, contest_number, discipline):
        self.request = request
        self.contest_number = contest_number
        self.discipline = discipline
        self.scramble_id = request.query_params.get('scramble_id')
        if self.scramble_id:
            self.scramble_id = int(self.scramble_id)
        self.reconstruction = request.data.get('reconstruction')
        self.time_ms = request.data.get('time_ms')
        self.dnf = request.data.get('dnf')
        print(request)

    def current_scrambles_and_solve(self):
        scrambles = ContestModel.objects.get(contest_number=self.contest_number).scramble_set.all()
        previous_solve = None
        for scramble in scrambles:
            solve = scramble.solve_set.filter(user=self.request.user.id).first()
            if not solve:
                if not previous_solve:
                    return None, scramble
                elif previous_solve.state == SOLVE_SUBMITTED_STATE:
                    return None, scramble
                elif previous_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                    while True:
                        extra_scramble = ScrambleModel.objects.get(id=previous_solve.extra_id)
                        extra_solve = extra_scramble.solve_set.filter(user=self.request.user.id).first()
                        if not extra_solve:
                            print(extra_solve, extra_scramble)
                            return extra_solve, extra_scramble
                        elif extra_solve.state == SOLVE_PENDING_STATE:
                            return extra_solve, extra_scramble
                        elif extra_solve.state == SOLVE_SUBMITTED_STATE:
                            print(None, scramble)
                            return None, scramble
                        elif extra_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                            previous_solve = extra_solve

            elif solve.state == SOLVE_PENDING_STATE:
                return solve, scramble
            previous_solve = solve

    def contest_is_finished(self):
        try:
            user_submitted_solves = (RoundSessionModel.objects.get(contest__contest_number=self.contest_number,
                                                        discipline__name=self.discipline, user=self.request.user.id)
                                            .solve_set.filter(user=self.request.user.id, state=SOLVE_SUBMITTED_STATE))
        except ObjectDoesNotExist:
            return False
        if len(user_submitted_solves) == SOLVES_IN_CONTEST:
            return True
        else:
            return False

    def create_solve(self):
        current_solve, current_scramble = self.current_scrambles_and_solve()
        if current_scramble and not current_solve:
            contest = ContestModel.objects.get(contest_number=self.contest_number)
            user = User.objects.get(id=self.request.user.id)
            discipline = DisciplineModel.objects.get(name=self.discipline)
            try:
                round_session = RoundSessionModel.objects.get(user=self.request.user.id, discipline__name=self.discipline,
                                                                contest__contest_number=self.contest_number)
            except ObjectDoesNotExist:
                round_session = RoundSessionModel(contest=contest, discipline=discipline, user=user)
                round_session.save()
            v = SolveValidator(scramble=current_scramble.moves, reconstruction=self.reconstruction)
            print(self.dnf)
            if self.dnf is True:
                solve = SolveModel(contest=contest, scramble=current_scramble,
                                   user=user, discipline=discipline, round_session=round_session, dnf=True)
            elif v.is_valid():
                solve = SolveModel(contest=contest, time_ms=self.time_ms, reconstruction=self.reconstruction,
                                   scramble=current_scramble, user=user, discipline=discipline, round_session=round_session)
            else:
                solve = SolveModel(contest=contest, scramble=current_scramble,
                                   user=user, discipline=discipline, round_session=round_session, dnf=True)

            solve.save()
            return solve.id
        else:
            # APIException.default_detail = ""
            APIException.status_code = 404
            raise APIException

    def update_solve(self):

        action = self.request.query_params.get('action')

        solve = (RoundSessionModel.objects.get(user=self.request.user.id, discipline__name=self.discipline
                                        , contest__contest_number=self.contest_number).solve_set.filter
                                        (user=self.request.user.id, state=SOLVE_PENDING_STATE).first())

        if action == 'submit':
            solve.state = SOLVE_SUBMITTED_STATE
            solve.save()
            return True
        elif action == 'change_to_extra':
            extras = ScrambleModel.objects.filter(contest__contest_number=self.contest_number, extra=True)
            if extras:
                for extra in extras:
                    extra_solve = extra.solve_set.filter(user=self.request.user.id).first()
                    if not extra_solve:
                        solve.state = SOLVE_CHANGED_TO_EXTRA_STATE
                        solve.extra_id = extra.id
                        solve.save()
                        return True
                    else:
                        pass
                APIException.default_detail = {'detail': 'all extras has been used'}
                APIException.status_code = 404
                raise APIException
            else:
                return False

    @atomic()
    def submit_round_session(self):
        contest_is_finished = self.contest_is_finished()
        round_session = (ContestModel.objects.get(contest_number=self.contest_number).round_session_set
                  .get(discipline__name=self.discipline, user=self.request.user.id))
        if contest_is_finished:
            solve_set = round_session.solve_set.filter(state=SOLVE_SUBMITTED_STATE, dnf=False).order_by('time_ms')
            sum_ms = 0
            dnf_count = 0
            lowest_solve = solve_set.first()
            highest_solve = solve_set.last()
            if len(solve_set) <= 3:
                round_session.dnf = True
                round_session.submitted = True
                round_session.save()
                return True
            elif len(solve_set) > 3:
                solve_set_modified = solve_set.exclude(pk__in=[lowest_solve.pk, highest_solve.pk])
                for solve in solve_set_modified:
                    sum_ms += solve.time_ms
                if len(solve_set) == 4:
                    sum_ms += highest_solve.time_ms
                elif len(solve_set) == 5:
                    print('solve set lin is 5')
                    pass
                print('solve set lin is ' + str(len(solve_set)))
                round_session.avg_ms = sum_ms/3
                round_session.submitted = True
                round_session.save()
                return True

            # for solve in solve_set:
            #     if solve.dnf:
            #         dnf_count += 1
            #         continue
            #     elif not lowest_solve:
            #         lowest_solve = solve.time_ms
            #         continue
            #     elif not highest_solve:
            #         highest_solve = solve.time_ms
            #         continue
            #     if solve.time_ms > lowest_solve:
            #         if solve.time_ms < highest_solve:
            #             sum_ms += solve.time_ms
            #         elif solve.time_ms > highest_solve:
            #             sum_ms += highest_solve
            #             highest_solve = solve.time_ms
            #         elif solve.time_ms == highest_solve:
            #             sum_ms += solve.time_ms
            #     elif solve.time_ms < lowest_solve:
            #         sum_ms += lowest_solve
            #         lowest_solve = solve.time_ms
            #     elif solve.time_ms == lowest_solve:
            #         sum_ms += solve.time_ms
            #
            # if dnf_count == 0:
            #     round_session.avg_ms = sum_ms/3
            # elif dnf_count == 1:
            #     sum_ms += highest_solve
            #     round_session.avg_ms += sum_ms/3
            # elif dnf_count >= 2:
            #     round_session.dnf = True
            #
            # round_session.submitted = True
            # round_session.save()
            # return True
        else:
            return False

    def create_round_session(self):
        contest = ContestModel.objects.get(contest_number=self.contest_number)
        discipline = DisciplineModel.objects.get(name=self.discipline)
        user = User.objects.get(id=self.requests.user.id)
        round_session = RoundSessionModel(contest=contest, discipline=discipline, user=user)
        round_session.save()
