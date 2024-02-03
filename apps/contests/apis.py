from rest_framework.views import APIView, Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
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
        contest_id = serializers.IntegerField()
        discipline_id = serializers.IntegerField()

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
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='contest_id',
                location=OpenApiParameter.QUERY,
                description='contest id',
                required=True,
                type=int,
            ),
            OpenApiParameter(
                name='discipline_id',
                location=OpenApiParameter.QUERY,
                description='discipline id',
                required=True,
                type=int,
            )
        ]
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        round_session_set = self.list_with_solves(filters=filters_serializer.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=round_session_set,
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
