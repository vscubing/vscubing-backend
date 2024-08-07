from django.core.management.base import BaseCommand
from apps.contests.tasks import create_contest


class Command(BaseCommand):
    help = 'generate new contest'

    def handle(self, *args, **options):
        create_contest()
