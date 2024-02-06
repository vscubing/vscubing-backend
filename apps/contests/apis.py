from collections import OrderedDict

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
    ContestSelector,
    SolveSelector,
)


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListApi(APIView):
    pass


class SolveRetrieveApi(APIView, SolveSelector):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        time_ms = serializers.IntegerField()
        is_dnf = serializers.BooleanField()
        submission_state = serializers.CharField()
        reconstruction = serializers.CharField()

        scramble = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        user = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        discipline = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        round_session = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        contest = inline_serializer(fields={
            'id': serializers.IntegerField()
        })

    @extend_schema(
        responses={200: OutputSerializer}
    )
    def get(self, request, pk):
        solve = self.retrieve(pk)
        data = self.OutputSerializer(solve).data
        return Response(data=data)


class SolveListBestInDiscipline(APIView, SolveSelector):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        time_ms = serializers.IntegerField()
        created_at = serializers.DateTimeField()
        user = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'username': serializers.CharField(),
        })
        scramble = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'scramble': serializers.CharField()
        })
        contest = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.CharField(),
        })
        discipline = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.CharField(),
        })

    @extend_schema(
        responses={200: OutputSerializer}
    )
    def get(self, request):
        solve_set = self.list_best_in_every_discipline()
        data = self.OutputSerializer(solve_set, many=True).data
        return Response(data=data)


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
        order_by = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        avg_ms = serializers.IntegerField()
        is_dnf = serializers.BooleanField()
        is_finished = serializers.BooleanField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

        user = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'username': serializers.CharField()  # add max_length
        })
        contest = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        discipline = inline_serializer(fields={
            'id': serializers.IntegerField()
        }),
        solve_set = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'is_dnf': serializers.BooleanField(),
            'submission_state': serializers.CharField(),
            'extra_id': serializers.IntegerField(),
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
            ),
            OpenApiParameter(
                name='order_by',
                location=OpenApiParameter.QUERY,
                description='order by something',
                type=str,
                enum=('avg_ms', '-avg_ms')
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


class RoundSessionRetrieveApi(APIView, RoundSessionSelector):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        avg_ms = serializers.IntegerField()
        is_dnf = serializers.BooleanField()
        is_finished = serializers.BooleanField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

        user = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'username': serializers.CharField()  # add max_length
        })
        contest = inline_serializer(fields={
            'id': serializers.IntegerField()
        })
        discipline = inline_serializer(fields={
            'id': serializers.IntegerField()
        }),
        solve_set = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'is_dnf': serializers.BooleanField(),
            'submission_state': serializers.CharField(),
            'extra_id': serializers.IntegerField(),
        })

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
            ),
            OpenApiParameter(
                name='user_id',
                location=OpenApiParameter.PATH,
                description='user_id',
                required=True,
                type=int,
            ),
        ]
    )
    def get(self, request, user_id):
        round_session = self.retrieve_with_solves(user_id=user_id, params=request.query_params)
        round_session_place = self.retrieve_place(user_id=user_id, params=request.query_params)
        print(round_session)
        print(round_session_place)
        data = self.OutputSerializer(round_session).data
        data['place'] = round_session_place
        return Response(data=data)


class RoundSessionProgresStateApi(APIView):
    @extend_schema(
        responses={200: {'json': 'data'}}
    )
    def get(self):
        return Response(data={'json': 'data'})


class ContestListApi(APIView, ContestSelector):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        order_by = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.CharField()

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='limit',
                location=OpenApiParameter.QUERY,
                description='count of contest to be returned',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='offset',
                location=OpenApiParameter.QUERY,
                description='offset',
                required=False,
                type=int,
            )
        ]
    )
    def get(self, request):
        filter_serializers = self.FilterSerializer(data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)
        contest_set = self.list(filters=filter_serializers.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=contest_set,
            request=request,
            view=self,
        )
