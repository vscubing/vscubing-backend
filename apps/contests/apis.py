from rest_framework.views import APIView, Response
from drf_spectacular.views import extend_schema
from rest_framework import serializers

from apps.core.utils import inline_serializer
from .paginators import (
    LimitOffsetPagination,
    get_paginated_response,
)
from .selectors import (
    RoundSessionSelector,
)


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListApi(APIView):
    pass


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveRetrieveApi(APIView):
    def get(self, request, pk):
        # selectors: select one solve by id
        # filters: filter with filter serializer
        # serializers: serialize
        return Response(data={'json': 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListBestInDisciplineList(APIView):
    def get(self, request):
        return Response(data={'json', 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListBestOfEveryUser(APIView):
    def get(self, request):
        return Response(data={'json', 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveCreateApi(APIView):
    def post(self, request):
        return Response(data={'json': 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveSubmitApi(APIView):
    def patch(self, request):
        return Response(data={'json': 'data'})


class RoundSessionWithSolvesListApi(APIView, RoundSessionSelector):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        pass

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        avg_ms = serializers.IntegerField()
        is_dnf = serializers.BooleanField()
        is_finished = serializers.BooleanField()

        user = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'username': serializers.CharField()  # add max_length
        })
        contest = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        discipline = inline_serializer(fields={
            'id': serializers.IntegerField()
        })

        class Meta:
            ref_name = 'contests.RoundSessionWithSolvesListOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()}
    )
    def get(self, request):
        # selectors: select all solves including round_sessions` data to every solve and then sort on frontend
        round_session_set = self.list_with_solves(params=request.query_params)
        # filters
        data = self.OutputSerializer(round_session_set, many=True).data
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=data,
            request=request,
            view=self
        )


@extend_schema(
    responses={200: {'json': 'data'}}
)
class RoundSessionProgresStateApi(APIView):
    def get(self):
        return Response(data={'json': 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class ContestListApi(APIView):
    def get(self, request):
        return Response(data={'json': 'data'})
