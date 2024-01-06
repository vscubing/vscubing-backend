import os

from dotenv import load_dotenv
from faker import Faker

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from allauth.socialaccount.models import SocialApp

from apps.accounts.models import User

load_dotenv()

USERS_QTY = 100


class Command(BaseCommand):
    help = 'Generate fake data for accounts app'

    def handle(self, *args, **options):
        self.fake = Faker()
        self.users()
        self.superuser()
        self.google_client()

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

    @atomic
    def google_client(self):
        print(SocialApp._meta.get_fields())
        social_app = SocialApp.objects.create(
            provider='google',
            name='google_cliend',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            secret=os.getenv('GOOGLE_SECRET_KEY'),
        )
        social_app.sites.set([1])
        social_app.save()
