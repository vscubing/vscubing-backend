from django.db.transaction import atomic

from vscubing.celery import app
from .models import ContestModel, DisciplineModel, ScrambleModel
from scripts.scramble import generate_scramble


@app.task
def add():
    @atomic()
    def create_contest():
        previous_contest = ContestModel.objects.order_by('contest_number').last()
        if previous_contest:
            previous_contest.ongoing = False
            previous_contest.save()
            new_contest = ContestModel(contest_number=previous_contest.contest_number + 1)
        else:
            new_contest = ContestModel(contest_number=1)
        new_contest.save()
        discipline = DisciplineModel.objects.get(name='3by3')
        for scramble_position in range(1, 6):
            generated_scramble = generate_scramble()
            scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                     extra=False, contest=new_contest, discipline=discipline)
            scramble.save()
        for scramble_position in range(1, 3):
            scramble_position = f"E{scramble_position}"
            generated_scramble = generate_scramble()
            scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                     extra=True, contest=new_contest, discipline=discipline)
            scramble.save()

    create_contest()
