from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import serializers

from apps.core.utils import inline_serializer
from apps.core.permissions import IsVerified
from .paginators import (
    LimitPagePagination,
    get_paginated_data,
)
from .selectors import (
    RoundSessionSelector,
    ContestSelector,
    SolveSelector,
    SingleResultLeaderboardSelector,
    ContestLeaderboardSelector,
    CurrentRoundSessionProgressSelector,
    AvailableDisciplinesListSelector
)
from .services import (
    CreateSolveService,
    SubmitSolveService,
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
            'id': serializers.IntegerField(),
            'moves': serializers.CharField(),
            'position': serializers.CharField()
        })
        user = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'username': serializers.CharField()
        })
        discipline = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'slug': serializers.CharField()
        })
        contest = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'slug': serializers.CharField()
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


class CreateSolveApi(APIView):
    # Api to create solve when user finished solving cube
    permission_classes = [IsAuthenticated, IsVerified]

    class InputSerializer(serializers.Serializer):
        reconstruction = serializers.CharField(required=False)
        is_dnf = serializers.BooleanField()
        time_ms = serializers.IntegerField(required=False)

        class Meta:
            ref_name = 'contests.CreateSolveInputSerializer'

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        is_dnf = serializers.BooleanField()
        time_ms = serializers.IntegerField()
        created_at = serializers.DateTimeField()
        scramble = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'moves': serializers.CharField()
        })

        class Meta:
            ref_name = 'contests.CreateSolveOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
        request=InputSerializer(),
        parameters=[
            OpenApiParameter(
                name='discipline_slug',
                location=OpenApiParameter.QUERY,
                description='discipline slug',
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name='scramble_id',
                location=OpenApiParameter.QUERY,
                description='scramble_id',
                required=True,
                type=int,
            ),
        ]
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CreateSolveService(
            user_id=request.user.id,
            discipline_slug=request.query_params.get('discipline_slug', None)
        )
        service.create_solve(
            scramble_id=request.query_params.get('scramble_id', None),
            **serializer.validated_data
        )
        return Response(status=status.HTTP_201_CREATED)


class SubmitSolveApi(APIView):
    # Api for submitting or rejecting solve
    permission_classes = [IsAuthenticated, IsVerified]

    class InputSerializer(serializers.Serializer):
        reason_for_taking_extra = serializers.CharField(max_length=1500, required=False)

        ref_name = 'contests.SubmitSolveInputSerializer'

    @extend_schema(
        responses={200: None},
        request=InputSerializer(),
        parameters=[
            OpenApiParameter(
                name='action',
                location=OpenApiParameter.QUERY,
                description='action',
                required=True,
                type=str,
                enum=['submit', 'change_to_extra']
            )
        ]
    )
    def post(self, request, solve_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = SubmitSolveService(
            solve_id=solve_id,
            user_id=request.user.id
        )
        service.submit_solve(action=request.query_params.get('action'),
                             user_id=request.user.id,
                             **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class ContestLeaderboardApi(APIView, RoundSessionSelector):
    # Api for contest dashboard to display finished round_sessions
    class Pagination(LimitPagePagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        discipline_slug = serializers.CharField()
        order_by = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        page_size = serializers.IntegerField()
        page = serializers.IntegerField()
        pages = serializers.IntegerField()
        results = inline_serializer(fields={
            'contest': inline_serializer(fields={
                'id': serializers.IntegerField(),
                'slug': serializers.CharField(),
                'start_date': serializers.DateTimeField(),
                'end_date': serializers.DateTimeField(),
                'discipline_set': inline_serializer(many=True, fields={
                    'id': serializers.IntegerField(),
                    'slug': serializers.CharField(),
                    'name': serializers.CharField(),
                })
            }),
            'own_result': inline_serializer(required=False, fields={
                'round_session': inline_serializer(fields={
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
                        'time_ms': serializers.IntegerField(),
                        'scramble': inline_serializer(fields={
                            'id': serializers.IntegerField(),
                            'position': serializers.CharField(),
                        })
                    })
                }),
                'place': serializers.IntegerField(),
                'is_displayed_separately': serializers.BooleanField(),
                'page': serializers.IntegerField()
            }),
            'round_session_set': inline_serializer(many=True, fields={
                'round_session': inline_serializer(fields={
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
                        'time_ms': serializers.IntegerField(),
                        'scramble': inline_serializer(fields={
                            'id': serializers.IntegerField(),
                            'position': serializers.CharField(),
                        })
                    })
                }),
                'place': serializers.IntegerField()
            })
        })

        class Meta:
            ref_name = 'contests.RoundSessionWithSolvesListOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='page',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='page size',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='contest_slug',
                location=OpenApiParameter.QUERY,
                description='contest slug',
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name='discipline_slug',
                location=OpenApiParameter.QUERY,
                description='discipline slug',
                required=True,
                type=str,
            )
        ]
    )
    def get(self, request):
        selector = ContestLeaderboardSelector()

        data = selector.leaderboard_retrieve(
            contest_slug=str(request.query_params.get('contest_slug', '1')),
            discipline_slug=str(request.query_params.get('discipline_slug', '3by3')),
            page_size=int(request.query_params.get('page_size', 10)),
            page=int(request.query_params.get('page', 1)),
            user_id=request.user.id
        )
        data = self.OutputSerializer(data).data

        return Response(data)


class ContestListApi(APIView, ContestSelector):
    # lists all existing contests
    class Pagination(LimitPagePagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        order_by = serializers.CharField(required=False)
        discipline_slug = serializers.CharField(required=True)

    class OutputSerializer(serializers.Serializer):
        page_size = serializers.IntegerField()
        page = serializers.IntegerField()
        pages = serializers.IntegerField()
        results = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.CharField(),
            'start_date': serializers.DateTimeField(),
            'end_date': serializers.DateTimeField(),
            'discipline_set': inline_serializer(many=True, fields={
                'id': serializers.IntegerField(),
                'slug': serializers.CharField(),
                'name': serializers.CharField(),
            })
        })

        class Meta:
            ref_name = 'contests.ContestListOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='page',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='page size',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='discipline_slug',
                location=OpenApiParameter.QUERY,
                description='discipline slug',
                required=True,
                type=str
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
        start_date = serializers.DateTimeField()
        end_date = serializers.DateTimeField()
        discipline_set = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'slug': serializers.CharField(),
            'name': serializers.CharField(),
        })

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


class CurrentRoundSessionProgressApi(APIView, SolveSelector):
    # Sends current scramble, all needed for solving information and solve if exists
    permission_classes = [IsAuthenticated, IsVerified]

    class OutputSerializer(serializers.Serializer):
        current_solve = inline_serializer(fields={
            'scramble': inline_serializer(fields={
                'id': serializers.IntegerField(),
                'is_extra': serializers.BooleanField(),
                'position': serializers.CharField(),
                'moves': serializers.CharField()
            }),
            'can_change_to_extra': serializers.BooleanField(),
            'solve': inline_serializer(required=False, fields={
                'id': serializers.IntegerField(),
                'is_dnf': serializers.BooleanField(),
                'time_ms': serializers.IntegerField(),
                'scramble': inline_serializer(fields={
                    'id': serializers.IntegerField(),
                    'is_extra': serializers.BooleanField(),
                    'position': serializers.CharField(),
                    'moves': serializers.CharField()
                }),
            })
        })
        submitted_solve_set = inline_serializer(required=False, many=True, fields={
            'solve': inline_serializer(fields={
                'id': serializers.IntegerField(),
                'is_dnf': serializers.BooleanField(),
                'time_ms': serializers.IntegerField(),
                'scramble': inline_serializer(fields={
                    'id': serializers.IntegerField(),
                    'is_extra': serializers.BooleanField(),
                    'position': serializers.CharField(),
                    'moves': serializers.CharField()
                }),
            })
        })

        class Meta:
            ref_name = 'contests.CurrentSolveOutputSerializer'
        
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
        ]
    )
    def get(self, request):
        selector = CurrentRoundSessionProgressSelector(
            user_id=request.user.id,
            discipline_slug=request.query_params.get('discipline_slug')
        )
        data = selector.retrieve_data()
        data = self.OutputSerializer(data).data
        return Response(data)


class SingleResultLeaderboardApi(APIView):
    class Pagination(LimitPagePagination):
        default_limit = 10

    class OutputSerializer(serializers.Serializer):
        page_size = serializers.IntegerField()
        page = serializers.IntegerField()
        pages = serializers.IntegerField()
        results = inline_serializer(fields={
            'own_result': inline_serializer(required=False, fields={
                'solve': inline_serializer(fields={
                    'id': serializers.IntegerField(),
                    'time_ms': serializers.IntegerField(),
                    'is_dnf': serializers.BooleanField(),
                    'contest': inline_serializer(fields={
                        'id': serializers.IntegerField(),
                        'slug': serializers.CharField()
                    }),
                    'created_at': serializers.DateTimeField(),
                }),
                'place': serializers.IntegerField(),
                'is_displayed_separately': serializers.BooleanField(),
                'page': serializers.IntegerField()
            }),

            'solve_set': inline_serializer(many=True, fields={
                'solve': inline_serializer(fields={
                    'id': serializers.IntegerField(),
                    'time_ms': serializers.IntegerField(),
                    'is_dnf': serializers.BooleanField(),
                    'created_at': serializers.DateTimeField(),
                    'user': inline_serializer(fields={
                                                  'id': serializers.IntegerField(),
                                                  'username': serializers.CharField(),
                                              }),
                    'contest': inline_serializer(fields={
                        'id': serializers.IntegerField(),
                        'slug': serializers.CharField()
                    }),
                }),
                'place': serializers.IntegerField()
            })
        })

        class Meta:
            ref_name = 'contests.SingleResultLeaderboardOutputSerializer'

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
                name='page_size',
                location=OpenApiParameter.QUERY,
                description='page size',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='page',
                required=False,
                type=int,
            )
        ]
    )
    def get(self, request):
        leaderboard_selector = SingleResultLeaderboardSelector(
            discipline_slug=request.query_params.get('discipline_slug', '3by3'),
            user_id=request.user.id
        )
        data = leaderboard_selector.leaderboard_retrieve(
            page_size=int(request.query_params.get('page_size', 10)),
            page=int(request.query_params.get('page', 1)),
        )
        data = self.OutputSerializer(data).data

        return Response(data, status=200)


class UserCapabilities(APIView):
    authentication_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        can_solve_ongoing_contest = serializers.BooleanField()

    def get(self):
        pass


class AvailableDisciplinesListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.CharField()

    @extend_schema(
        responses={200: OutputSerializer(many=True)})

    def get(self, request):
        selector = AvailableDisciplinesListSelector()
        discipline_set = selector.discipline_set_retrieve()
        data = self.OutputSerializer(discipline_set, many=True).data
        return Response(data)
