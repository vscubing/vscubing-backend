from dotenv import load_dotenv
from django.db.transaction import atomic
from django.core.management.base import BaseCommand


from apps.contests.models import (
    TnoodleScramblesModel
)
from scripts.scramble import generate_scramble

load_dotenv()

USERS_QTY = 25
DISCIPLINE_NAMES = ['3by3']
TNOODLE_SCRAMBLES = 50000
CONTEST_QTY = 25


class Command(BaseCommand):
    help = 'Generate Tnoodle scrambles'
    @atomic()
    def handle(self, *args, **options):
        self.tnoodle_scrambles()

    def tnoodle_scrambles(self):
        for i in range(0, TNOODLE_SCRAMBLES):
            scramble_moves = generate_scramble(moves_count=23)
            print(scramble_moves)
            TnoodleScramblesModel.objects.create(moves=scramble_moves)
