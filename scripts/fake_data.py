# create discipline

# create contest
# create scrambles

# create fake solves

import sys
import random

from apps.contests.models import ScrambleModel, ContestModel, DisciplineModel, SolveModel
from apps.accounts.models import User

from .scramble import generate_scramble


def create_contest():
    previous_contest = ContestModel.objects.order_by('name').last()
    new_contest = ContestModel(name=previous_contest.name + 1)
    new_contest.save()


def create_contest_scrambles():
    previous_contest = ContestModel.objects.order_by('name').last()
    discipline = DisciplineModel.objects.get(name='3by3')
    for num in range(1, 6):
        generated_scramble = generate_scramble()
        scramble = ScrambleModel(num=num, scramble=generated_scramble, extra=False, contest=previous_contest, discipline=discipline)
        scramble.save()
    for num in range(1, 3):
        generated_scramble = generate_scramble()
        scramble = ScrambleModel(num=num, scramble=generated_scramble, extra=True, contest=previous_contest, discipline=discipline)
        scramble.save()


def create_solves():
    users = User.objects.all()
    discipline = DisciplineModel.objects.get(name='3by3')

    contest = ContestModel.objects.order_by('name').last()
    for user in users:
        for scramble in contest.scramble_set.all():
            if not scramble.extra:
                time_ms = random.randrange(25000, 200000)
                solve = SolveModel(time_ms=time_ms, dnf=False, state='submitted', reconstruction=scramble.scramble,
                                   contest=contest, scramble=scramble, user=user, discipline=discipline)
                solve.save()
                print(solve)


def scratch_setup():
    pass
