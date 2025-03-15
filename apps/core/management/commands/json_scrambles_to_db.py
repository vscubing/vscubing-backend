import json
from django.db.transaction import atomic
from django.core.management.base import BaseCommand

from apps.contests.models import TnoodleScramblesModel, DisciplineModel

class Command(BaseCommand):
    @atomic()
    def add_arguments(self, parser):
        parser.add_argument(
            '--discipline_name',
            type=str,
            required=True,  # Makes this argument mandatory
            help='Discipline name (required)',
        )

    def handle(self, *args, **options):
        input_filename = 'apps/core/management/commands/scrambles.json'
        discipline_name = options['discipline_name']  # Ensure this is a single string
        discipline = DisciplineModel.objects.get(name=discipline_name)

        with open(input_filename, 'r') as file:
            json_data = json.load(file)

        scrambles = []
        for event in json_data['wcif']['events']:
            for round in event['rounds']:
                for scramble_set in round['scrambleSets']:
                    scrambles.extend(scramble_set['scrambles'])
                    scrambles.extend(scramble_set['extraScrambles'])

        for scramble in scrambles:
            TnoodleScramblesModel.objects.create(moves=scramble, discipline=discipline)

