# creates contest from tnoodle scrambles (official creation)

from django.core.management.base import BaseCommand
from apps.contests.general_services import generate_contest_service

class Command(BaseCommand):
    help = 'trigger contest generation function'

    def handle(self, *args, **options):
        generate_contest_service()
