import os

from allauth.socialaccount.models import SocialApp
from dotenv import load_dotenv
import random
from datetime import timedelta
from django.db.transaction import atomic
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker

from apps.contests.models import (
    ContestModel,
    SolveModel,
    DisciplineModel,
    ScrambleModel,
    RoundSessionModel
)
from apps.accounts.models import User
from config import SOLVE_SUBMITTED_STATE
from scripts.scramble import generate_scramble

load_dotenv()

USERS_QTY = 10
DISCIPLINE_NAMES = ['3by3']
CONTEST_QTY = 5


class Command(BaseCommand):
    help = 'Generate fake data for accounts app'
    @atomic()
    def handle(self, *args, **options):
        self.fake = Faker()
        self.users()
        self.superuser()
        self.google_client()

        self.disciplines()
        for i in range(CONTEST_QTY):
            self.contest_scrambles_sessions_solves()

    def users(self):
        for user in range(USERS_QTY):
            User.objects.create(
                username=self.fake.unique.user_name(),
                email=self.fake.unique.email(),
                is_verified=True,
                is_active=True,
                is_staff=False,
            )

    def superuser(self):
        user = User.objects.create(
            username='1',
            email='1@gmail.com',
            is_superuser=True,
            is_verified=True,
            is_active=True,
            is_staff=True,
        )
        user.set_password('1')
        user.save()

    @atomic
    def google_client(self):
        print(SocialApp._meta.get_fields())
        social_app = SocialApp.objects.create(
            provider='google',
            name='google_client',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            secret=os.getenv('GOOGLE_SECRET_KEY'),
        )
        social_app.sites.set([1])
        social_app.save()

    def disciplines(self):
        if not DisciplineModel.objects.all():
            for discipline in DISCIPLINE_NAMES:
                DisciplineModel.objects.create(
                    name=discipline,
                    slug=discipline
                )
        else:
            pass

    def contest_scrambles_sessions_solves(self):
        last_contest = ContestModel.objects.last()
        name = 1
        if last_contest:
            name = str(int(last_contest.name) + 1)
            last_contest.is_ongoing = False
            last_contest.save()
            start_date = last_contest.start_date
        else:
            start_date = timezone.now()

        end_date = start_date + timedelta(days=7)
        contest = ContestModel.objects.create(
            name=name,
            slug=name,
            start_date=start_date,
            end_date=end_date
        )

        discipline = DisciplineModel.objects.get(name='3by3')
        for scramble_position in range(1, 6):
            generated_scramble = generate_scramble()
            scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                     is_extra=False, contest=contest, discipline=discipline)
            scramble.save()
        for scramble_position in range(1, 3):
            scramble_position = f"E{scramble_position}"
            generated_scramble = generate_scramble()
            scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                     is_extra=True, contest=contest, discipline=discipline)
            scramble.save()

        users = User.objects.all()

        for user in users:
            discipline = DisciplineModel.objects.get(name='3by3')
            round_session = RoundSessionModel.objects.create(
                contest=contest,
                discipline=discipline,
                user=user,
                is_finished=True
            )
            random_time = random.uniform(8, 100)

            scrambles = ScrambleModel.objects.filter(contest=contest, discipline=discipline, is_extra=False)
            for scramble in scrambles:
                solve = SolveModel.objects.create(
                    time_ms=round(random.uniform(random_time*random.uniform(0.7, 1.3), random_time*random.uniform(0.7, 1.3)), 3)*1000,
                    is_dnf=False,
                    submission_state='submitted',
                    scramble=scramble,
                    user=user,
                    discipline=discipline,
                    round_session=round_session,
                    contest=contest,
                    reconstruction=scramble
                )
                sum_ms = 0
            solve_set = round_session.solve_set.filter(submission_state=SOLVE_SUBMITTED_STATE, is_dnf=False).order_by('time_ms')
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
                round_session.avg_ms = sum_ms / 3
                round_session.submitted = True
                round_session.save()
