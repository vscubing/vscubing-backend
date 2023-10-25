from rest_framework.views import APIView, Response, status

from apps.accounts.models import User
from .models import ContestModel, SolveModel, DisciplineModel, ScrambleModel
from .serializers import dashboard_serializers, contest_serializers, solve_contest_serializers, solve_reconstruction_serializers
from .permissions import ContestPermission, SolveContestPermission
from .validators import CurrentSolveValidator, SaveSolveValidator
from config import SOLVE_SUBMITTED_STATE


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
        solves = contest.solve_set.filter(state=SOLVE_SUBMITTED_STATE, discipline__name=discipline).order_by('user_id', 'time_ms')
        serializer = contest_serializers.ContestSubmittedSolvesSerializer(solves, many=True)
        return Response(serializer.data)


class SolveContestView(APIView):
    permission_classes = [SolveContestPermission]

    def get(self, request, contest_number, discipline):
        submitted_solves = User.objects.get(id=request.user.id).solve_set.filter(contest__contest_number=contest_number,
                                                               discipline__name=discipline, state=SOLVE_SUBMITTED_STATE)
        contest_scrambles = ContestModel.objects.get(contest_number=contest_number).scramble_set.all()
        current_solve_validator = CurrentSolveValidator(scrambles=contest_scrambles, request=request)
        current_solve, current_scramble = current_solve_validator.find_current_scrambles()

        submitted_solves_serializer = solve_contest_serializers.SubmittedSolveSerializer(submitted_solves, many=True)
        try:
            current_solve_serializer = solve_contest_serializers.CurrentSolveSerializer(current_solve).data
        except AttributeError:
            current_solve_serializer = None
        current_scramble_serializer = solve_contest_serializers.CurrentScrambleSerializer(current_scramble)

        return Response({'submitted_solves': submitted_solves_serializer.data,
                         'current_solve': {'scramble': current_scramble_serializer.data,
                                            'solve': current_solve_serializer}})

    def post(self, request, contest_number, discipline):
        # TODO make solve validation with checking scrambles sequence and if solve mach scramble

        solve_validator = SaveSolveValidator(request, contest_number, discipline)
        solve_validator.create()

        return Response(status=status.HTTP_200_OK)


class OngoingContestNumberView(APIView):
    def get(self, request):
        ongoing_contest = ContestModel.objects.filter(ongoing=True).last()
        return Response(ongoing_contest.contest_number)


class SolveReconstructionSerializer(APIView):
    def get(self, request, id):
        solve = SolveModel.objects.get(id=id)
        serializer = solve_reconstruction_serializers.SolveSerializer(solve)
        return Response(serializer.data)
