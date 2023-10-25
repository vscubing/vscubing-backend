from django.shortcuts import redirect

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


class SolveValidator:
    def __init__(self, request, contest_number, discipline):
        self.request = request
        self.contest_number = contest_number
        self.discipline = discipline
        self.scramble_id = request.query_params.get('scramble_id')
        self.reconstruction = request.data.get('reconstruction')
        self.time_ms = request.data.get('time_ms')
        print(request)

    def find_current_scrambles(self):
        self.scrambles = ContestModel.objects.get(contest_number=self.contest_number).scramble_set.all()
        previous_solve = None
        for scramble in self.scrambles:
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

    def is_valid(self):
        pass

    def contest_is_finished(self):
        solves = (ContestModel.objects.get(contest_number=self.contest_number)
                  .solve_set.filter(user=self.request.user.id, state=SOLVE_SUBMITTED_STATE))
        if len(solves) == 5:
            return True
        else:
            return False

    def submit_contest(self):
        solves = (ContestModel.objects.get(contest_number=self.contest_number)
                  .solve_set.filter(user=self.request.user.id, state=SOLVE_SUBMITTED_STATE))
        if len(solves) == 5:
            for solve in solves:
                solve.contest_submitted = True
                solve.save()
            return True
        else:
            return False

    def create(self):
        solve = SolveModel(time_ms=self.time_ms, reconstruction=self.reconstruction,
                           scramble=ScrambleModel.objects.get(id=self.scramble_id),
                           contest=ContestModel.objects.get(contest_number=self.contest_number),
                           user=User.objects.get(id=self.request.user.id),
                           discipline=DisciplineModel.objects.get(name=self.discipline))
        solve.save()
        return solve

    def update(self):

        action = self.request.query_params.get('action')
        solve_id = self.request.data.get('solve_id')
        solve = SolveModel.objects.get(id=solve_id, user=self.request.user.id, state=SOLVE_PENDING_STATE)
        if action == 'submit':
            solve.state = SOLVE_SUBMITTED_STATE
            solve.save()
        elif action == 'change_to_extra':
            extras = ScrambleModel.objects.filter(contest__contest_number=self.contest_number, extra=True)
            for extra in extras:
                if not extra.solve_set.filter(user=self.request.user.id).first():
                    solve.state = SOLVE_CHANGED_TO_EXTRA_STATE
                    solve.extra_id = extra.id
                    print('saving solve')
                    solve.save()
                    return True
                else:
                    print(extra)
