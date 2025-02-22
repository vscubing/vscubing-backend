from django.utils import timezone
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from apps.contests.general_selectors import current_contest_retrieve
from apps.contests.models import (
    ContestModel,
    DisciplineModel,
    ScrambleModel,
)


class Command(BaseCommand):
    help = 'generate new contest'

    def handle(self, *args, **options):
        self.generate_contest()


    @atomic()
    def generate_contest(self, days_lasts=1):
        current_contest = current_contest_retrieve()
        if current_contest:
            name_and_slug = str(int(current_contest.slug) + 1)
        elif not current_contest:
            name_and_slug = 1
        if current_contest:
            name_and_slug = str(int(current_contest.name) + 1)
            current_contest.is_ongoing = False
            current_contest.save()
            start_date = current_contest.start_date
        else:
            start_date = timezone.now()

        end_date = start_date + timedelta(days=days_lasts)
        contest = ContestModel.objects.create(
            name=name_and_slug,
            slug=name_and_slug,
            start_date=start_date,
            end_date=end_date
        )

        discipline = DisciplineModel.objects.get(name='3x3')
        new_scrambles_moves = 'R2 L2'
        inx = 1
        scramble_position = '1'
        is_extra = False
        for i in range(0, 7):
            if inx < 6:
                scramble_position = str(inx)
                is_extra = False
                print('no extra')
            elif inx >= 6:
                print('extra')
                is_extra = True
                if inx == 6:
                    scramble_position = 'E1'
                elif inx == 7:
                    scramble_position = 'E2'
            scramble = ScrambleModel(position=scramble_position, moves=new_scrambles_moves,
                                     is_extra=is_extra, contest=contest, discipline=discipline)
            scramble.save()
            inx += 1
