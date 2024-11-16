import json

from django.core.management.base import BaseCommand

from apps.contests.models import TnoodleScramblesModel

class Command(BaseCommand):
    def handle(self, *args, **options):
        input_filename = 'apps/core/management/commands/scrambles.json'
        with open(input_filename, 'r') as file:
            json_data = json.load(file)

        scrambles = []
        for event in json_data['wcif']['events']:
            for round in event['rounds']:
                for scramble_set in round['scrambleSets']:
                    scrambles.extend(scramble_set['scrambles'])
                    scrambles.extend(scramble_set['extraScrambles'])

        for scramble in scrambles:
            scramble = TnoodleScramblesModel.objects.create(moves=scramble)
