import time

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
from rest_framework.views import APIView, Response, status
from django.db.transaction import atomic

from apps.accounts.models import User
from .models import ContestModel, SolveModel, DisciplineModel, ScrambleModel
from .serializers import dashboard_serializers, contest_serializers, solve_contest_serializers, solve_reconstruction_serializers
from .permissions import ContestPermission, SolveContestPermission
from .managers import SolveManager
from config import SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE
from scripts.scramble import generate_scramble
from scripts.cube import SolveValidator


class DashboardView(APIView):

    def get(self, request):
        contests = ContestModel.objects.all()
        disciplines = DisciplineModel.objects.all()

        solve_set = []
        for discipline in disciplines:
            solve = discipline.solve_set.order_by('time_ms').first()
            if solve:
                solve_set.append(solve)

        contests_serializer = dashboard_serializers.ContestSerializer(contests, many=True)
        best_solves_serializer = dashboard_serializers.BestSolvesSerializer(solve_set, many=True)
        return Response({'contests': contests_serializer.data, 'best_solves': best_solves_serializer.data})


class ContestView(APIView):
    permission_classes = [ContestPermission]

    def get(self, request, contest_number, discipline):
        contest = ContestModel.objects.get(contest_number=contest_number)
        solves = contest.round_set.filter(submitted=True, state=SOLVE_SUBMITTED_STATE,
                                          discipline__name=discipline).order_by('user_id', 'id')
        serializer = contest_serializers.ContestSubmittedSolvesSerializer(solves, many=True)
        return Response(serializer.data)


class SolveContestView(APIView):
    permission_classes = [SolveContestPermission]

    def get(self, request, contest_number, discipline):
        submitted_solves = User.objects.get(id=request.user.id).solve_set.filter(contest__contest_number=contest_number,
                                                               discipline__name=discipline, state=SOLVE_SUBMITTED_STATE)
        current_solve_validator = SolveManager(request=request, contest_number=contest_number, discipline=discipline)
        current_solve, current_scramble = current_solve_validator.current_scrambles_and_solve()
        solves_changed_to_extra = (ContestModel.objects.get(contest_number=contest_number)
                                        .solve_set.filter(user=request.user.id,
                                        discipline__name=discipline, state=SOLVE_CHANGED_TO_EXTRA_STATE))
        if len(solves_changed_to_extra) >= 2:
            can_change_to_extra = False
        else:
            can_change_to_extra = True

        submitted_solves_serializer = solve_contest_serializers.SubmittedSolveSerializer(submitted_solves, many=True)
        try:
            current_solve_serializer = solve_contest_serializers.CurrentSolveSerializer(current_solve).data
        except AttributeError:
            current_solve_serializer = None
        current_scramble_serializer = solve_contest_serializers.ScrambleSerializer(current_scramble)

        return Response({'submitted_solves': submitted_solves_serializer.data,
                         'current_solve': {'scramble': current_scramble_serializer.data,
                         'solve': current_solve_serializer, 'can_change_to_extra': can_change_to_extra}})

    def post(self, request, contest_number, discipline):
        solve_manager = SolveManager(request, contest_number, discipline)
        solve_id = solve_manager.create_solve()
        if solve_id:
            return Response({'solve_id': solve_id}, status=status.HTTP_200_OK)
        else:
            APIException.default_detail = "wrong scramble provided"
            APIException.status_code = 400
            raise APIException

    def put(self, request, contest_number, discipline):
        validator = SolveManager(request, contest_number, discipline)
        start_time = time.time()
        solve_updated = validator.update_solve()
        print(time.time() - start_time)
        if solve_updated:
            contest_is_finished = validator.contest_is_finished()
            if contest_is_finished:
                validator.submit_contest()
                return Response({'detail': 'contest submitted'}, status=status.HTTP_200_OK)
            else:
                request.method = 'GET'
                return self.get(request, contest_number, discipline)
        else:
            APIException.default_detail = 'solve is not updated'
            APIException.status_code = 404
            raise APIException


class OngoingContestNumberView(APIView):
    def get(self, request):
        ongoing_contest = ContestModel.objects.filter(ongoing=True).last()
        return Response(ongoing_contest.contest_number)


class SolveReconstructionSerializer(APIView):
    def get(self, request, id):
        try:
            solve = SolveModel.objects.get(id=id)
        except ObjectDoesNotExist:
            APIException.status_code = 404
            raise APIException
        serializer = solve_reconstruction_serializers.SolveSerializer(solve)
        return Response(serializer.data)


class NewContestView(APIView):
    def post(self, request):
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
