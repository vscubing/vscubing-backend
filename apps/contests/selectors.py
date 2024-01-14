from django.db.models import Subquery, OuterRef

from config import SOLVE_SUBMITTED_STATE
from .models import SolveModel, DisciplineModel
from .paginators import solve_paginator


class SolveSelector:  # One service for one model

    def solve_list(self, params):
        queryset = SolveModel.objects.all()
        queryset = solve_paginator(queryset=queryset, params=params)
        return queryset

    def solve_list_bests_in_disciplines(self):
        disciplines = DisciplineModel.objects.all()
        queryset = []
        for discipline in disciplines:
            solve = SolveModel.objects.order_by('time_ms').filter(discipline=discipline.id).first()
            queryset.append(solve)
        return queryset

    def solve_list_every_user_best(self, params):
        discipline_name = params.get('discipline_name')
        # TODO Not constant speed of db reads
        best_solves = SolveModel.objects.filter(
            user_id=OuterRef('user_id'),
            discipline__name=discipline_name,
            state=SOLVE_SUBMITTED_STATE,
            dnf=False,
            round_session__submitted=True,

        ).order_by('time_ms').values('id')[:1]
        queryset = SolveModel.objects.filter(
            id__in=Subquery(best_solves)
        )
        queryset = solve_paginator(queryset=queryset, params=params)

        return queryset

    def solve_retrieve(self, pk):
        queryset = SolveModel.objects.get(id=pk)
        return queryset
