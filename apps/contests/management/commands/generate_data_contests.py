from django.core.management.base import BaseCommand
from faker import Faker
from apps.contests.models import ContestModel, SolveModel, DisciplineModel, ScrambleModel, RoundSessionModel
from apps.accounts.models import User

DISCIPLINE_NAMES = ['3by3']
CONTEST_QTY = 20


class Command(BaseCommand):
    help = 'Generate fake data for contests app'

    def handle(self, *args, **kwargs):
        self.fake = Faker()

        # self.disciplines()
        self.contests()
        self.ongoing_contest()
        self.scrambles()
        self.contest_crambles_sessions_solves()
        self.solve()

    def disciplines(self):
        for discipline in DISCIPLINE_NAMES:
            DisciplineModel.objects.create(
                name=discipline
            )

    def contests(self):
        pass

    def ongoing_contest(self):
        pass

    def scrambles(self):
        pass

    def round_sessions_and_solves(self):
        pass

    def solve(self):
        pass

    def contest_crambles_sessions_solves(self):
        last_contest = ContestModel.objects.last()
        contest_number = 1
        if last_contest:
            contest_number = last_contest.contest_number + 1
            last_contest.ongoing=False
            last_contest.save()

        ContestModel.objects.create(
            contest_number=contest_number,

        )

