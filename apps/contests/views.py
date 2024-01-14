import time

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery, OuterRef
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.views import APIView, Response, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.db.transaction import atomic

from apps.accounts.models import User
from .models import ContestModel, SolveModel, DisciplineModel, ScrambleModel, RoundSessionModel
from .permissions import ContestPermission, SolveContestPermission
from .managers import SolveManager
from .selectors import SolveSelector
from config import SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE
from scripts.scramble import generate_scramble
from .serializers import SolveSerializer, ScrambleSerializer01, RoundSessionSerializer01, ContestSerializer01, DisciplineSerializer01


class DisciplineViewSet(ViewSet):
    def list(self, request):
        queryset = DisciplineModel.objects.all()
        serializer = DisciplineSerializer01(queryset, many=True)
        return Response(serializer.data)


class ContestViewSet(ViewSet):
    def list(self, request):
        queryset = ContestModel.objects.all()
        serializer = ContestSerializer01(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = ContestModel.objects.get(id=pk)
        serializer = ContestSerializer01(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ongoing_contest(self, request):
        queryset = ContestModel.objects.filter(ongoing=True).last()
        serializer = ContestSerializer01(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def new_contest(self, request):
        @atomic()
        def create_contest():
            previous_contest = ContestModel.objects.order_by('contest_number').last()
            if previous_contest:
                previous_contest.ongoing = False
                previous_contest.save()
                new_contest = ContestModel(contest_number=previous_contest.contest_number + 1)
            else:
                new_contest = ContestModel(contest_number=1)
            new_contest.save()
            discipline = DisciplineModel.objects.get(name='3by3')
            for scramble_position in range(1, 6):
                generated_scramble = generate_scramble()
                scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                         extra=False, contest=new_contest, discipline=discipline)
                scramble.save()
            for scramble_position in range(1, 3):
                scramble_position = f"E{scramble_position}"
                generated_scramble = generate_scramble()
                scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                         extra=True, contest=new_contest, discipline=discipline)
                scramble.save()

        create_contest()
        return Response('new contest created')


class RoundSessionViewSet(ViewSet):
    @action(detail=False, methods=['delete'])
    def delete_user_session(self, request):
        last_contest = ContestModel.objects.last()
        round_session = RoundSessionModel.objects.filter(contest=last_contest, user=request.user.id)
        if round_session:
            round_session.delete()
            return Response('resource deleted successfully', status=status.HTTP_202_ACCEPTED)
        else:
            APIException.status_code = 400
            APIException.default_detail = 'dont exists'

    @action(detail=False, methods=['get'])
    def round_sessions_with_solves(self, request):
        discipline_name = request.query_params.get('discipline_name')
        contest_number = request.query_params.get('contest_number')
        round_session_set = RoundSessionModel.objects.filter(discipline__name=discipline_name, submitted=True,
                                                             contest__contest_number=contest_number)
        serializer = RoundSessionSerializer01(round_session_set, many=True,
                                              fields=['id', 'solve_set', 'discipline', 'avg_ms'],
                                              solve_set_fields=['id', 'time_ms', 'dnf', 'state', 'scramble', 'created'],
                                              user_fields=['username'])

        return Response(serializer.data)


class ScrambleViewSet(ViewSet):
    pass


class SolveViewSet(ViewSet):
    def list(self, request):
        scramble = SolveModel.objects.all()
        serializer = SolveSerializer(scramble, many=True, fields=['id', 'scramble'])
        return Response(serializer.data)

    def retrieve(self, reqeust, pk):
        queryset = SolveModel.objects.get(id=pk)
        serializer = SolveSerializer(queryset, fields=['id'])
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[SolveContestPermission])
    def solve_progress(self, request):
        contest_number = ContestModel.objects.filter(ongoing=True).last().contest_number
        discipline = request.query_params.get('discipline')
        current_solve_manager = SolveManager(request=request, contest_number=contest_number, discipline=discipline)
        contest_is_finished = current_solve_manager.contest_is_finished()
        print(contest_is_finished)
        if current_solve_manager.contest_is_finished():
            session_submitted = current_solve_manager.submit_round_session()
            if session_submitted:
                pass
            elif not session_submitted:
                APIException.default_detail = "Round Session can't be submitted"
                APIException.status_code = 500
                raise APIException
        else:
            pass

        current_solve, current_scramble = current_solve_manager.current_scrambles_and_solve()

        try:
            round_session = (User.objects.get(id=request.user.id)
                             .round_session_set.get
                             (contest__contest_number=contest_number,
                              discipline__name=discipline))
            solves_changed_to_extra = round_session.solve_set.filter(user=request.user.id,
                                       discipline__name=discipline, state=SOLVE_CHANGED_TO_EXTRA_STATE)
            submitted_solves = round_session.solve_set.filter(state=SOLVE_SUBMITTED_STATE)
        except ObjectDoesNotExist:
            solves_changed_to_extra = []
            submitted_solves = []
        if len(solves_changed_to_extra) >= 2:
            can_change_to_extra = False
        else:
            can_change_to_extra = True
        submitted_solves_serializer = SolveSerializer(submitted_solves, many=True,
                                                      fields=('id', 'time_ms', 'dnf', 'scramble'),
                                                      scramble_fields=('id', 'scramble', 'extra', 'position')).data
        try:
            if current_solve is not None:
                current_solve_serializer = SolveSerializer(current_solve, fields=('id', 'time_ms', 'dnf')).data
            else:
                current_solve_serializer = None
        except AttributeError:
            current_solve_serializer = None
        current_scramble_serializer = ScrambleSerializer01(current_scramble).data

        return Response({'submitted_solves': submitted_solves_serializer,
                         'current_solve': {'scramble': current_scramble_serializer,
                         'solve': current_solve_serializer, 'can_change_to_extra': can_change_to_extra}})

    @action(detail=False, methods=['post'], permission_classes=[SolveContestPermission])
    def create_solve(self, request):
        discipline_name = request.query_params.get('discipline_name')
        contest_number = request.query_params.get('contest_number')
        solve_manager = SolveManager(request, contest_number, discipline_name)
        solve_id = solve_manager.create_solve()
        if solve_id:
            return Response({'solve_id': solve_id}, status=status.HTTP_200_OK)
        else:
            APIException.default_detail = "wrong scramble provided"
            APIException.status_code = 400
            raise APIException

    @action(detail=True, methods=['patch'], permission_classes=[SolveContestPermission])
    def submit_solve(self, request):
        contest_number = ContestModel.objects.filter(ongoing=True).last().contest_number
        discipline = request.query_params.get('discipline')

        manager = SolveManager(request, contest_number, discipline)
        start_time = time.time()
        solve_updated = manager.update_solve()
        print(time.time() - start_time)
        if solve_updated:
            contest_is_finished = manager.contest_is_finished()
            if contest_is_finished:
                manager.submit_round_session()
                return Response({'detail': 'contest submitted'}, status=status.HTTP_200_OK)
            else:
                request.method = 'GET'
                return self.get(request, contest_number, discipline)
        else:
            APIException.default_detail = 'solve is not updated'
            APIException.status_code = 404
            raise APIException

    @action(detail=TypeError, methods=['get'])
    def solve_reconstruction(self, request, pk):
        try:
            solve = SolveModel.objects.get(id=pk)
        except ObjectDoesNotExist:
            APIException.status_code = 404
            raise APIException
        serializer = SolveSerializer(solve, fields=['id', 'reconstruction', 'contest_number', 'created'],
                                     scramble_fields=['scramble', 'position'],
                                     discipline_fields=['name'],
                                     user_fields=['username'])
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def best_solves_in_discipline(self, request):
        disciplines = DisciplineModel.objects.all()

        solve_set = []
        for discipline in disciplines:
            solve = discipline.solve_set.order_by('time_ms').filter(state=SOLVE_SUBMITTED_STATE,
                                                                    round_session__submitted=True,
                                                                    dnf=False).first()
            if solve:
                solve_set.append(solve)

        best_solves_serializer = SolveSerializer(solve_set, many=True,
                                                 fields=['id', 'time_ms', 'scramble', 'contest_number', 'created'],
                                                 scramble_fields=['id'],
                                                 discipline_fields=['name'],
                                                 user_fields=['username']
                                                 )
        return Response(best_solves_serializer.data)

    @action(detail=False, methods=['get'])
    def every_user_best_solve(self, request):
        discipline_name = request.query_params.get('discipline_name')
        best_solves = SolveModel.objects.filter(
            user_id=OuterRef('user_id'),
            discipline__name=discipline_name,
            state=SOLVE_SUBMITTED_STATE,
            dnf=False,
            round_session__submitted=True,

        ).order_by('time_ms').values('id')[:1]

        all_solves = SolveModel.objects.filter(
            id__in=Subquery(best_solves)
        )

        print(all_solves)
        serializer = SolveSerializer(all_solves, many=True,
                                     fields=['id', 'time_ms', 'created'],
                                     user_fields=['id', 'username'],
                                     scramble_fields=['id', 'scramble'],
                                     contest_fields=['contest_number'],
                                     discipline_fields=['name']
                                     )
        return Response(serializer.data)


# solve related apis


class SolveListApi(APIView, SolveSelector):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SolveModel
            fields = '__all__'

    def get(self, request):
        queryset = self.solve_list(params=request.query_params)
        data = self.OutputSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class SolveListBestOfEveryUserApi(APIView):  # needs to be renamed
    pass


class SolveListBestsInDisciplinesApi(APIView):
    pass


class SolveRetrieveApi(APIView):
    pass


class SolveCreateApi(APIView):
    pass


class SolveSubmitApi(APIView):
    pass
