from django.db.models import Subquery, OuterRef

from config import SOLVE_SUBMITTED_STATE
from .models import SolveModel, DisciplineModel
from .serializers import SolveSerializer
from .paginators import solve_paginator


class SolveService():  # One service for one model
    def solve_create(self):
        pass

    def solve_partial_update(self):
        pass

    def solve_update(self):
        pass

    def solve_list(self):

        if self.params.get('best_solves_in_disciplines'):
            disciplines = DisciplineModel.objects.all()
            queryset = []
            for discipline in disciplines:
                solve = SolveModel.objects.order_by('time_ms').filter(discipline=discipline.id).first()
                queryset.append(solve)
            serializer = SolveSerializer(data=queryset, many=True)
            serializer.is_valid()
            return serializer

        elif self.params.get('every_user_best_solve'):
            discipline_name = self.params.get('discipline_name')
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
            serializer = SolveSerializer(data=queryset, many=True)
            serializer.is_valid()

            return serializer

        else:
            queryset = SolveModel.objects.all()
            queryset = solve_paginator(queryset=queryset, params=self.params)
            serializer = SolveSerializer(data=queryset, many=True)
            serializer.is_valid()
            return serializer

    def solve_retrieve(self):
        pass

    def solve_delete(self):
        pass
