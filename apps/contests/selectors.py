from django.db.models import Subquery, OuterRef

from config import SOLVE_SUBMITTED_STATE
from .models import SolveModel, DisciplineModel
from .paginators import solve_paginator


class SolveSelector:  # One service for one model

    def solve_list(self, params):
        queryset = SolveModel.objects.all()
        queryset = solve_paginator(queryset=queryset, params=params)
        return queryset

    def solve_retrieve(self):
        pass
