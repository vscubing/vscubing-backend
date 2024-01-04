from django.core.management.base import BaseCommand
from faker import Faker
from apps.contests.models import ContestModel, SolveModel, DisciplineModel, ScrambleModel, RoundSessionModel
from apps.accounts.models import User

USERS_QTY = 100


class Command(BaseCommand):
    help = 'Generate fake data for accounts app'

    def handle(self, *args, **options):
        self.fake = Faker()
        self.users()

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
        User.objects.create(
            username='1',
            email='1@gmail.com',
            password='1',
            is_superuser=True,
            is_verified=True,
            is_active=True,
            is_staff=True,
        )
