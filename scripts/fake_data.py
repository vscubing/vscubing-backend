# create discipline

# create contest
# create scrambles

# create fake solves

import sys
import random

from apps.contests.models import ScrambleModel, ContestModel, DisciplineModel, SolveModel

from .scramble import generate_scramble


def create_contest():
    previous_contest = ContestModel.objects.order_by('name').first()
    new_contest = ContestModel(name=previous_contest.name + 1)
    new_contest.save()


def create_contest_scrambles():
    previous_contest = ContestModel.objects.order_by('name').first()
    discipline = DisciplineModel.objects.get(name='3by3')
    for num in range(1, 6):
        generated_scramble = generate_scramble()
        scramble = ScrambleModel(num=num, scramble=generated_scramble, extra=False, contest=previous_contest, discipline=discipline)
        scramble.save()
    for num in range(1, 3):
        generated_scramble = generate_scramble()
        scramble = ScrambleModel(num=num, scramble=generated_scramble, extra=True, contest=previous_contest, discipline=discipline)
        scramble.save()
