from rest_framework.exceptions import APIException

from config import SOLVE_PENDING_STATE, SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE
from .models import ScrambleModel, SolveModel, ContestModel, DisciplineModel
from apps.accounts.models import User

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
        print(request)

    def current_scrambles_and_solve(self):
        scrambles = ContestModel.objects.get(contest_number=self.contest_number).scramble_set.all()
        previous_solve = None
        for scramble in scrambles:
            solve = scramble.solve_set.filter(user=self.request.user.id).first()
            if not solve:
                if not previous_solve:
                    return solve, scramble
                elif previous_solve.state == SOLVE_SUBMITTED_STATE:
                    return solve, scramble
                elif previous_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                    extra_scramble = ScrambleModel.objects.get(id=previous_solve.extra_id)
                    extra_solve = extra_scramble.solve_set.filter(user=self.request.user.id).first()
                    if not extra_solve:
                        return extra_solve, extra_scramble
                    elif extra_solve.state == SOLVE_PENDING_STATE:
                        return extra_solve, extra_scramble
                    elif extra_solve.state == SOLVE_SUBMITTED_STATE:
                        print(solve, scramble)
                        return solve, scramble

            elif solve.state == SOLVE_PENDING_STATE:
                return solve, scramble
            previous_solve = solve

    def contest_is_finished(self):
        user_submitted_solves = ContestModel.objects.get(contest_number=self.contest_number.solve_set.filter(user=self.request.user.id, state=SOLVE_SUBMITTED_STATE))
        if len(user_submitted_solves) == 5:
            return True
        else:
            return False

    def create_solve(self):
        current_solve, current_scramble = self.current_scrambles_and_solve()
        if current_scramble.id == self.scramble_id and not current_solve:
            scramble = ScrambleModel.objects.get(id=self.scramble_id)
            contest = ContestModel.objects.get(contest_number=self.contest_number)
            user = User.objects.get(id=self.request.user.id)
            discipline = DisciplineModel.objects.get(name=self.discipline)
            solve = SolveModel(time_ms=self.time_ms, reconstruction=self.reconstruction, scramble=scramble,
                               contest=contest, user=user, discipline=discipline)
            solve.save()
            return solve.id
        else:
            # APIException.default_detail = ""
            APIException.status_code = 404
            raise APIException

    def update_solve(self):

        action = self.request.query_params.get('action')
        solve = (ContestModel.objects.get(contest_number=self.contest_number).
                 solve_set.filter(user=self.request.user.id, state=SOLVE_PENDING_STATE).first())
        if action == 'submit':
            solve.state = SOLVE_SUBMITTED_STATE
            solve.save()
            return True
        elif action == 'change_to_extra':
            extras = ScrambleModel.objects.filter(contest__contest_number=self.contest_number, extra=True)
            for extra in extras:
                extra_solves = extra.solve_set.filter(user=self.request.user.id).first()
                if not extra_solves:
                    solve.state = SOLVE_CHANGED_TO_EXTRA_STATE
                    solve.extra_id = extra.id
                    solve.save()
                    return True
                else:
                    pass
            return False

    def submit_contest(self):
        contest_is_finished = self.contest_is_finished()
        solves = (ContestModel.objects.get(contest_number=self.contest_number)
                  .solve_set.filter(user=self.request.user.id))
        if contest_is_finished:
            for solve in solves:
                solve.contest_submitted = True
                solve.save()
            return True
        else:
            return False

    def reconstruction_is_valid(self):
        return None
