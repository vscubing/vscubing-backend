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
    RoundSessionModel,
    SingleResultLeaderboardModel,
    TnoodleScramblesModel
)
from apps.accounts.models import User
from config import SOLVE_SUBMITTED_STATE
from scripts.scramble import generate_scramble

load_dotenv()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--users_qty', type=int, default=25, help='Number of users')
        parser.add_argument('--discipline_names', type=str, nargs='+', default=['3by3', '2by2' ], help='List of discipline names')
        parser.add_argument('--tnoodle_scrambles_qty', type=int, default=30, help='Number of tnoodle scrambles')
        parser.add_argument('--tnoodle_scrambles_moves_qty', type=int, default=5, help='Number of moves in each tnoodle scramble')
        parser.add_argument('--scrambles_moves_qty', type=int, default=3, help='Number of moves in scramble')
        parser.add_argument('--contest_qty', type=int, default=15, help='Number of contests')

    help = 'Generate fake data for accounts app'
    @atomic()
    def handle(self, *args, **options):
        self.users_qty = options['users_qty']
        self.discipline_names = options['discipline_names']
        self.tnoodle_scrambles_qty = options['tnoodle_scrambles_qty']
        self.tnoodle_scrambles_moves_qty = options['tnoodle_scrambles_moves_qty']
        self.contest_qty = options['contest_qty']
        self.fake = Faker()
        self.users()
        self.superuser()
        self.google_client()
        self.disciplines()
        for i in range(self.contest_qty):
            self.contest_scrambles_sessions_solves()
        self.single_solve_leaderboard()
        self.tnoodle_scrambles()

    def users(self):
        for user in range(self.users_qty):
            User.objects.create(
                username=self.fake.unique.user_name(),
                email=self.fake.unique.email(),
                is_verified=True,
                is_active=True,
                is_staff=False,
            )

    def superuser(self):
        user, created = User.objects.get_or_create(
            username='1',
            email='1@gmail.com',
            defaults={
                'is_superuser': True,
                'is_verified': True,
                'is_active': True,
                'is_staff': True,
            }
        )

        if created:
            user.set_password('1')
            user.save()



    @atomic
    def google_client(self):
        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            name='google_client',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            secret=os.getenv('GOOGLE_SECRET_KEY'),
        )
        print(social_app, created)
        social_app.sites.set([1])
        social_app.save()

    def disciplines(self):
        if not DisciplineModel.objects.all():
            for discipline in self.discipline_names:
                DisciplineModel.objects.create(
                    name=discipline,
                    slug=discipline
                )
        else:
            pass

    def contest_scrambles_sessions_solves(self):
        discipline_set = DisciplineModel.objects.all()
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
        contest.discipline_set.add(*discipline_set)
        contest.save()

        for discipline in discipline_set:
            for scramble_position in range(1, 6):
                generated_scramble = generate_scramble(moves_count=self.tnoodle_scrambles_moves_qty)
                scramble = ScrambleModel(position=scramble_position, moves=generated_scramble,
                                         is_extra=False, contest=contest, discipline=discipline)
                scramble.save()
            for scramble_position in range(1, 3):
                scramble_position = f"E{scramble_position}"
                generated_scramble = generate_scramble(moves_count=self.tnoodle_scrambles_moves_qty)
                scramble = ScrambleModel(position=scramble_position, moves=generated_scramble,
                                         is_extra=True, contest=contest, discipline=discipline)
                scramble.save()

        users = User.objects.all()

        def reverse_scramble(scramble):
            moves = scramble.split()
            inverse_moves = {
                "R": "R'", "R'": "R", "R2": "R2",
                "L": "L'", "L'": "L", "L2": "L2",
                "U": "U'", "U'": "U", "U2": "U2",
                "D": "D'", "D'": "D", "D2": "D2",
                "F": "F'", "F'": "F", "F2": "F2",
                "B": "B'", "B'": "B", "B2": "B2"
            }
            solving_algorithm = [inverse_moves[move] for move in reversed(moves)]
            return ' '.join(solving_algorithm)

        for user in users:
            for discipline in DisciplineModel.objects.all():
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
                        reconstruction=reverse_scramble(scramble.moves)
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

    def single_solve_leaderboard(self):
        users = User.objects.all()
        for user in users:
            best_solve = SolveModel.objects.filter(user=user).order_by('time_ms').first()
            if best_solve:
                SingleResultLeaderboardModel.objects.get_or_create(solve=best_solve, time_ms=best_solve.time_ms)
            else:
                pass

    def tnoodle_scrambles(self):
        discipline_set = DisciplineModel.objects.all()
        for discipline in discipline_set:
            for i in range(0, self.tnoodle_scrambles_qty):
                scramble_moves = generate_scramble(moves_count=self.tnoodle_scrambles_moves_qty)
                print(scramble_moves)
                TnoodleScramblesModel.objects.create(moves=scramble_moves, discipline=discipline)
