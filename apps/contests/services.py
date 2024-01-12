from django.db.models import Subquery, OuterRef

from config import SOLVE_SUBMITTED_STATE
from .models import SolveModel, DisciplineModel
from .serializers import SolveSerializer, SolveWithRelatedFieldsSerializer
from .paginators import solve_paginator


class SolveService:  # One service for one model
    def create_solve(self):
        pass

    def partial_update_solve(self):
        pass

    def update_solve(self):
        pass

    def list_solve(self, params, user):

        if params.get('best_solves_in_disciplines'):
            disciplines = DisciplineModel.objects.all()
            queryset = []
            for discipline in disciplines:
                solve = SolveModel.objects.order_by('time_ms').filter(discipline=discipline.id).first()
                queryset.append(solve)
            serializer = SolveWithRelatedFieldsSerializer(data=queryset, many=True)
            serializer.is_valid()
            return serializer

        elif params.get('every_user_best_solve'):
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
            serializer = SolveSerializer(data=queryset, many=True)
            serializer.is_valid()

            return serializer

        else:
            queryset = SolveModel.objects.all()
            queryset = solve_paginator(queryset=queryset, params=params)
            serializer = SolveSerializer(data=queryset, many=True)
            serializer.is_valid()
            return serializer

    def retrieve_solve(self):
        pass

    def delete_solve(self):
        pass
