from django.utils import timezone
from datetime import timedelta
from django.db.transaction import atomic

from .general_selectors import current_contest_retrieve
from .models import (
    TnoodleScramblesModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
)


@atomic()
def generate_contest_service(days_lasts=7):
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

    discipline = DisciplineModel.objects.get(name='3by3')
    tnoodle_scrambles = TnoodleScramblesModel.objects.filter(is_used=False)[0:7]
    inx = 1
    scramble_position = '1'
    for tnoodle_scramble in tnoodle_scrambles:
        scramble = ScrambleModel(position=scramble_position, moves=tnoodle_scramble.moves,
                                 is_extra=True, contest=contest, discipline=discipline)
        inx += 1
        if inx < 6:
            scramble_position = str(inx)
        elif inx >= 6:
            if inx == 6:
                scramble_position = 'E1'
            elif inx == 7:
                scramble_position = 'E2'
        tnoodle_scramble.is_used = True
        tnoodle_scramble.save()
        scramble.save()
