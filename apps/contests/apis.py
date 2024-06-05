from collections import OrderedDict

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import serializers

from apps.core.utils import inline_serializer
from .paginators import (
    LimitOffsetPagination,
    LimitPagePagination,
    get_paginated_data,
)
from .selectors import (
    RoundSessionSelector,
    ContestSelector,
    SolveSelector,
    ScrambleSelector,
    SingleResultLeaderboardSelector
)
from .services import (
    SolveService,
    RoundSessionService
)


class SolveRetrieveApi(APIView, SolveSelector):
    # Should be a class for retrieving solve by pk
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

        class Meta:
            ref_name = 'contests.SolveRetrieveOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer}
    )
    def get(self, request, pk):
        solve = self.retrieve(pk)
        data = self.OutputSerializer(solve).data
        return Response(data=data)


class SolveListBestInEveryDiscipline(APIView, SolveSelector):
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
            'moves': serializers.CharField()
        })
        contest = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.CharField(),
        })
        discipline = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.CharField()
        })

        class Meta:
            ref_name = 'contests.SolveListBestInEveryDisciplineSerializer'

    @extend_schema(
        responses={200: OutputSerializer(many=True)}
    )
    def get(self, request):
        solve_set = self.list_best_in_every_discipline()
        data = self.OutputSerializer(solve_set, many=True).data
        return Response(data=data)


class SolveCurrentRetrieveApi(APIView):
    class OutputSerializer(serializers.Serializer):
        pass

    def get(self, request):
        data = {}
        data = self.OutputSerializer(data).data
        return Response(data)


class SolveCreateApi(APIView, SolveService):
    # Api to create solve when user finished solving cube
    class InputSerializer(serializers.Serializer):
        reconstruction = serializers.CharField()
        is_dnf = serializers.BooleanField()
        time_ms = serializers.IntegerField()

        class Meta:
            ref_name = 'contests.SolveCreateInputSerializer'

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        time_ms = serializers.IntegerField()
        created_at = serializers.DateTimeField()
        scramble = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'moves': serializers.CharField()
        })

        class Meta:
            ref_name = 'contests.SolveCreateOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
        request={InputSerializer()},
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
                name='scramble_id',
                location=OpenApiParameter.QUERY,
                description='scramble id',
                required=True,
                type=int,
            ),
        ]
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        solve = self.solve_create(request.query_params, **serializer.validated_data, user_id=request.uesr)
        data = self.OutputSerializer(solve).data
        return Response(data=data)


class SolveSubmitApi(APIView):
    # Api for submitting or rejecting solve
    @extend_schema(
        responses={200: {'json': 'data'}}
    )
    def patch(self, request):
        return Response(data={'json': 'data'})


class ContestLeaderboardApi(APIView, RoundSessionSelector):
    # Api for contest dashboard to display finished round_sessions
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        discipline_slug = serializers.CharField()
        order_by = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        limit = serializers.IntegerField()
        offset = serializers.IntegerField()
        count = serializers.IntegerField()
        next = serializers.CharField()
        previous = serializers.CharField()
        results = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'avg_ms': serializers.IntegerField(),
            'is_dnf': serializers.BooleanField(),
            'is_finished': serializers.BooleanField(),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),

            'user': inline_serializer(fields={
                'id': serializers.IntegerField(),
                'username': serializers.CharField(),
            }),

            'contest': inline_serializer(fields={
                'id': serializers.IntegerField(),
            }),

            'discipline': inline_serializer(fields={
                'id': serializers.IntegerField(),
            }),

            'solve_set': inline_serializer(many=True, fields={
                'id': serializers.IntegerField(),
                'is_dnf': serializers.BooleanField(),
                'submission_state': serializers.CharField(),
                'extra_id': serializers.IntegerField(),
            })})

        class Meta:
            ref_name = 'contests.RoundSessionWithSolvesListOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='discipline_slug',
                location=OpenApiParameter.QUERY,
                description='discipline slug',
                required=True,
                type=str,
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
    def get(self, request, contest_slug):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        round_session_set = self.contest_leaderboard(contest_slug, filters=filters_serializer.validated_data)
        data = get_paginated_data(
            pagination_class=self.Pagination,
            queryset=round_session_set,
            request=request,
            view=self
        )
        data = self.OutputSerializer(data).data

        return Response(data)


class ContestListApi(APIView, ContestSelector):
    # lists all existing contests
    class Pagination(LimitPagePagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        order_by = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        limit = serializers.IntegerField()
        page = serializers.IntegerField()
        count = serializers.IntegerField()
        next = serializers.CharField()
        previous = serializers.CharField()
        results = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.CharField(),
            'start_date': serializers.DateTimeField(),
            'end_date': serializers.DateTimeField(),
        })

        class Meta:
            ref_name = 'contests.ContestListOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='count of contest to be returned',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='limit',
                location=OpenApiParameter.QUERY,
                description='offset',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='order_by',
                location=OpenApiParameter.QUERY,
                description='order by something',
                type=str,
                enum=('created_at', '-created_at')
            )
        ]
    )
    def get(self, request):
        filter_serializers = self.FilterSerializer(data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)
        contest_set = self.list(filters=filter_serializers.validated_data)
        data = get_paginated_data(
            pagination_class=self.Pagination,
            queryset=contest_set,
            request=request,
            view=self,
        )
        
        data = self.OutputSerializer(data).data
        return Response(data)


class OngoingContestRetrieveApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        slug = serializers.CharField()

        class Meta:
            ref_name = 'OngoingContestRetrieveSerializer'

    @extend_schema(
        responses={200: OutputSerializer()}
    )
    def get(self, request):
        contest_selector = ContestSelector()
        current_contest = contest_selector.current_retrieve()
        data = self.OutputSerializer(current_contest).data
        return Response(data)


class CurrentSolveApi(APIView, SolveSelector):
    # Sends current scramble, all needed for solving information and solve if exists
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        current_scramble = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'is_extra': serializers.BooleanField(),
            'position': serializers.CharField(),
            'moves': serializers.CharField()
        })
        info = inline_serializer(fields={
            'can_change_to_extra': serializers.BooleanField(),
        })
        current_solve = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'is_dnf': serializers.BooleanField(),
            'time_ms': serializers.IntegerField(),
        })
        
    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='discipline_slug',
                location=OpenApiParameter.QUERY,
                description='discipline slug',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='contest_slug',
                location=OpenApiParameter.QUERY,
                description='contest slug',
                required=True,
                type=str
            ),
        ]
    )
    def get(self, request):

        solve_selector = SolveSelector()
        scramble_selector = ScrambleSelector()

        current_solve = solve_selector.retrieve_current(
            user_id=request.user.id,
            contest_slug=request.query_params['contest_slug'],
            discipline_slug=request.query_params['discipline_slug'],
        )

        current_scramble = scramble_selector.retrieve_current(
            user_id=request.user.id,
            contest_slug=request.query_params['contest_slug'],
            discipline_slug=request.query_params['discipline_slug'],
        )
        can_change_to_extra = solve_selector.can_change_current_to_extra(
            user_id=request.user.id,
            contest_slug=request.query_params['contest_slug'],
            discipline_slug=request.query_params['discipline_slug'],
        )

        info = {'can_change_to_extra': can_change_to_extra}
        data_bunch = {'current_solve': current_solve, 'current_scramble': current_scramble, 'info': info}
        data = self.OutputSerializer(data_bunch).data
        return Response(data)


class SubmittedSolvesApi(APIView):
    # Api to send submitted solves of the ongoing contest
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        is_dnf = serializers.BooleanField()
        scramble = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'is_extra': serializers.BooleanField(),
            'position': serializers.CharField(),
            'scramble': serializers.CharField()
        })

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='discipline_slug',
                location=OpenApiParameter.QUERY,
                description='discipline slug',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='contest_slug',
                location=OpenApiParameter.QUERY,
                description='contest slug',
                required=False,
                type=str
            ),
        ]
    )
    def get(self, request):
        solve_selector = SolveSelector()
        solve_set = solve_selector.onging_contest_submitted(
            user_id=request.user.id,
            contest_slug=request.query_params['contest_slug'],
            discipline_slug=request.query_params['discipline_slug']
        )
        data = self.OutputSerializer(solve_set, many=True).data
        return Response(data)


class SingleResultLeaderboardApi(APIView):
    class Pagination(LimitPagePagination):
        default_limit = 10

    class OutputSerializer(serializers.Serializer):
        limit = serializers.IntegerField()
        page = serializers.IntegerField()
        pages = serializers.IntegerField()
        results = inline_serializer(fields={
            'own_solve': inline_serializer(fields={
                'solve': inline_serializer(fields={
                    'id': serializers.IntegerField(),
                    'time_ms': serializers.IntegerField(),
                    'is_dnf': serializers.BooleanField(),
                    'submission_state': serializers.CharField(),
                    'reconstruction': serializers.CharField(),
                    'contest': inline_serializer(fields={
                            'id': serializers.IntegerField()
                        }),
                }),
                'place': serializers.IntegerField(),
                'is_displayed_separately': serializers.BooleanField(required=False),
                'page': serializers.IntegerField(required=False)
            }),

            'solve_set': inline_serializer(many=True, fields={
                'solve': inline_serializer(fields={
                    'id': serializers.IntegerField(),
                    'time_ms': serializers.IntegerField(),
                    'is_dnf': serializers.BooleanField(),
                    'submission_state': serializers.CharField(),
                    'reconstruction': serializers.CharField(),

                    'scramble': inline_serializer(fields={
                            'id': serializers.IntegerField()
                        }),
                    'user': inline_serializer(fields={
                                                  'id': serializers.IntegerField(),
                                                  'username': serializers.CharField(),
                                              }),
                    'contest': inline_serializer(fields={
                            'id': serializers.IntegerField()
                        }),
                }),
                'place': serializers.IntegerField(default=None)
            })
        })

        class Meta:
            ref_name = 'contests.SingleResultLeaderboardOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='limit',
                location=OpenApiParameter.QUERY,
                description='how many solves will be on the page',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='page number',
                required=False,
                type=int,
            )
        ]
    )
    def get(self, request):
        leaderboard_selector = SingleResultLeaderboardSelector()
        data = leaderboard_selector.leaderboard_retrieve(
            limit=int(request.query_params['limit']),
            page=int(request.query_params['page']),
            user_id=request.user.id
        )
        print(data)
        data = self.OutputSerializer(data).data

        return Response(data, status=200)
