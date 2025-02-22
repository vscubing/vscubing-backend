from django.utils import timezone
from datetime import timedelta
from django.db.transaction import atomic

from .general_selectors import current_contest_retrieve
from .services import SingleResultLeaderboardService
from .models import (
    TnoodleScramblesModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
)


@atomic()
def generate_contest_service(days_lasts=7):
    discipline_set = DisciplineModel.objects.all()
    current_contest = current_contest_retrieve()
    if current_contest:
        name_and_slug = str(int(current_contest.slug) + 1)
    elif not current_contest:
        name_and_slug = 1
    if current_contest:
        name_and_slug = str(int(current_contest.name) + 1)
        single_result_leaderboard_servie = SingleResultLeaderboardService()
        single_result_leaderboard_servie.update()
        current_contest.is_ongoing = False
        current_contest.save()
        start_date = timezone.now().replace(hour=19, minute=0, second=0, microsecond=0)
    else:
        start_date = timezone.now().replace(hour=19, minute=0, second=0, microsecond=0)

    end_date = (start_date + timedelta(days=days_lasts)).replace(hour=19, minute=0, second=0, microsecond=0)
    contest = ContestModel.objects.create(
        name=name_and_slug,
        slug=name_and_slug,
        start_date=start_date,
        end_date=end_date
    )
    contest.discipline_set.add(*discipline_set)
    contest.save()

    for discipline in discipline_set:
        tnoodle_scrambles = TnoodleScramblesModel.objects.filter(is_used=False, discipline=discipline)[0:7]
        inx = 1
        scramble_position = '1'
        is_extra = False
        for tnoodle_scramble in tnoodle_scrambles:
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
            tnoodle_scramble.is_used = True
            tnoodle_scramble.save()
            scramble = ScrambleModel(position=scramble_position, moves=tnoodle_scramble.moves,
                                     is_extra=is_extra, contest=contest, discipline=discipline)
            scramble.save()
            inx += 1
