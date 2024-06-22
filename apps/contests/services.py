from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError as DjangoValidationError
from django.http.response import HttpResponseServerError
from django.db.transaction import atomic

from .general_selectors import (
    current_contest_retrieve,
    retrieve_current_scramble,
    can_change_solve_to_extra
)
from .models import (
    RoundSessionModel,
    SolveModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
    SingleResultLeaderboardModel
)
from scripts.cube import ReconstructionValidator

User = get_user_model()


class CreateSolveService:
    def __init__(self, user_id, discipline_slug):
        self.user = User.objects.get(id=user_id)
        try:
            self.discipline = DisciplineModel.objects.get(slug=discipline_slug)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist
        self.contest = current_contest_retrieve()
        if not self.round_session_is_finished():
            pass
        else:
            raise PermissionDenied
        self.current_scramble = self.retrieve_current_scramble()
        self.round_session = self.retrieve_current_round_session()

    def create_solve(self, scramble_id, reconstruction, is_dnf, time_ms):
        """
        - check for authorization details (or raise 401) +
        - check if user can solve contest (or raise 403) +
        - find current contest (or raise 404 or 500 (need to decide)) +
        - check if this solve is for right scramble (or raise 400) +
        - validate solve moves correctness (if not save as dnf and send TODO something)
        - save solve +
        - save solve to round_session (mb as an atomic transaction with 4.)
        - return solve
        """
        # validate scramble
        if self.scramble_is_correct(scramble_id=scramble_id):
            pass
        else:
            raise DjangoValidationError
        # validate that scramble wasn't solved yes
        if self.solve_does_not_exists():
            pass
        else:
            raise PermissionDenied('solve already exists')
        # validate solve reconstruction
        solve_is_valid = self.solve_is_valid(
            reconstruction=reconstruction,
            time_ms=time_ms
        )
        if solve_is_valid:
            pass
        else:
            is_dnf = True

        solve = SolveModel.objects.create(
            time_ms=time_ms,
            is_dnf=is_dnf,
            reconstruction=reconstruction,
            submission_state='pending',

            user=self.user,
            contest=self.contest,
            discipline=self.discipline,
            round_session=self.round_session,
            scramble=self.current_scramble,
        )
        # TODO add solve to current_round_session
        return solve

    def round_session_is_finished(self):
        try:
            round_session = RoundSessionModel.objects.get(
                contest=self.contest,
                discipline=self.discipline,
                user=self.user,
            )
            return round_session.is_finished
        except ObjectDoesNotExist:
            return False

    def retrieve_current_scramble(self):
        current_scramble = retrieve_current_scramble(
            user=self.user,
            contest=self.contest
        )
        return current_scramble

    def scramble_is_correct(self, scramble_id):
        try:
            scramble = ScrambleModel.objects.get(id=scramble_id)
        except ObjectDoesNotExist:
            raise DjangoValidationError
        if scramble == self.current_scramble:
            return True
        else:
            return False

    def solve_is_valid(self, reconstruction, time_ms):
        reconstruction_validator = ReconstructionValidator(
            scramble=self.current_scramble.moves,
            reconstruction=reconstruction,
        )
        if reconstruction_validator.is_valid():
            return True
        else:
            return False

    def solve_does_not_exists(self):
        try:
            solve = self.contest.solve_set.get(
                discipline=self.discipline,
                user=self.user,
                scramble=self.current_scramble,
            )
            return False
        except ObjectDoesNotExist:
            return True

    def create_round_session(self):
        round_session = RoundSessionModel.objects.create(
                contest=self.contest,
                discipline=self.discipline,
                user=self.user,
            )
        return round_session

    def retrieve_current_round_session(self):
        try:
            round_session = RoundSessionModel.objects.get(
                contest=self.contest,
                discipline=self.discipline,
                user=self.user,
            )
            return round_session
        except ObjectDoesNotExist:
            round_session = self.create_round_session()
            return round_session


class SubmitSolveService:

    def __init__(self, discipline_slug, solve_id, user_id):
        try:
            self.user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist()

        self.current_contest = current_contest_retrieve()

        try:
            self.solve = SolveModel.objects.get(id=solve_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist()

    @atomic()
    def submit_solve(self, action):
        if self.solve.user == self.user:
            pass
        else:
            raise PermissionDenied()

        if self.solve.contest.is_ongoing:
            pass
        elif not self.solve.contest.is_ongoing:
            return DjangoValidationError('this contest has finished')
        else:
            return HttpResponseServerError

        if self.solve.submission_state == 'pending':
            pass
        else:
            raise DjangoValidationError('solve is already submitted')

        if action == 'submit':
            self.solve.submission_state = 'submitted'
        elif action == 'change_to_extra':
            if can_change_solve_to_extra(self.solve.contest, self.solve.discipline, self.user):
                self.solve.submission_state = 'changed_to_extra'
            else:
                raise PermissionDenied('cannot change to extra: all extra attempts were used')
        else:
            raise DjangoValidationError('wrong action chosen')

        self.solve.save()
        self.add_solve_to_round_session()

        self.add_solve_to_leaderboard()

    def add_solve_to_round_session(self):
        try:
            round_session = self.solve.contest.round_session_set.get(user=self.user)
        except ObjectDoesNotExist:
            round_session = self.create_round_session()

        self.solve.round_session = round_session
        self.solve.save()

    def create_round_session(self):
        contest = self.solve.contest
        discipline = self.solve.discipline
        user = self.user

        round_session = RoundSessionModel.objects.create(contest=contest, discipline=discipline, user=user)
        return round_session

    def round_session_is_finished(self):
        round_session = self.solve.round_sessoin
        solve_set = round_session.solve_set.filter(
            contest=self.solve.contest,
            discipline=self.solve.discipline,
            user=self.user,
            submission_state='submitted'
        )
        if len(solve_set) == 5:
            return True
        else:
            return False

    def finish_round_session(self):
        self.solve.round_session.is_finished = True
        self.solve.round_session.save()

    def add_solve_to_leaderboard(self):
        try:
            best_user_solve = SingleResultLeaderboardModel.objects.get(
                solve__user=self.user
            )
            if best_user_solve.solve.time_ms > self.solve:
                best_user_solve.delete()
                SingleResultLeaderboardModel.objects.create(
                    solve=self.solve,
                    time_ms=self.solve.time_ms
                )
            else:
                pass
        except ObjectDoesNotExist:
            SingleResultLeaderboardModel.objects.create(
                solve=self.solve,
                time_ms=self.solve.time_ms
            )


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

