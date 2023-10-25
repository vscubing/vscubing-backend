from config import SOLVE_PENDING_STATE, SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE
from .models import ScrambleModel, SolveModel, ContestModel, DisciplineModel
from apps.accounts.models import User

'''
all cases

1. no previous solve, send first scramble
2. current solve is pending, return current solve and scramble
3. previous solve is submitted, return current solve and scramble
4. previous solve is changed_to_extra, search for extra by id (in change to extra field). If extra is submitted go ahead
'''


class CurrentSolveValidator:
    def __init__(self, scrambles, request):
        self.request = request
        self.scrambles = scrambles

    def find_current_scrambles(self):
        previous_solve = None
        for scramble in self.scrambles:
            solve = scramble.solve_set.filter(user=self.request.user.id).first()
            if not solve:
                if not previous_solve:
                    return solve, scramble
                elif previous_solve.state == SOLVE_SUBMITTED_STATE:
                    return solve, scramble
                elif previous_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                    scramble = ScrambleModel.objects.get(id=previous_solve.extra_id)
                    return solve, scramble
            elif solve.state == SOLVE_PENDING_STATE:
                return solve, scramble
            previous_solve = solve


class SolveValidator:
    def __init__(self, request, contest_number, discipline):
        self.request = request
        self.contest_number = contest_number
        self.discipline = discipline
        self.scramble_id = request.query_params.get('scramble_id')
        self.reconstruction = request.data.get('reconstruction')
        self.time_ms = request.data.get('time_ms')
        print(request)

    def is_valid(self):
        pass

    def create(self):
        solve = SolveModel(time_ms=self.time_ms, reconstruction=self.reconstruction,
                           scramble=ScrambleModel.objects.get(id=self.scramble_id),
                           contest=ContestModel.objects.get(contest_number=self.contest_number),
                           user=User.objects.get(id=self.request.user.id),
                           discipline=DisciplineModel.objects.get(name=self.discipline))
        solve.save()

    def update(self):
        action = self.request.query_params.get('action')
        solve_id = self.request.data.get('solve_id')
        solve = SolveModel.objects.get(id=solve_id, user=self.request.user.id, state=SOLVE_PENDING_STATE)
        if action == 'submit':
            solve.state = SOLVE_SUBMITTED_STATE
            solve.save()
        elif action == 'change_to_extra':
            solve.state = SOLVE_CHANGED_TO_EXTRA_STATE
            solve.save()
