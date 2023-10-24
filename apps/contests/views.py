from rest_framework.views import APIView, Response, status

from .models import ContestModel, SolveModel, DisciplineModel
from .serializers import dashboard_serializers, contest_serializers, solve_contest_serializers, solve_reconstruction_serializers
from .permissions import ContestPermission, SolveContestPermission


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
        solves = contest.solve_set.filter(state='contest_submitted', discipline__name=discipline).order_by('user_id', 'time_ms')
        serializer = contest_serializers.ContestSubmittedSolvesSerializer(solves, many=True)
        return Response(serializer.data)


class SolveReconstructionSerializer(APIView):
    def get(self, request, id):
        solve = SolveModel.objects.get(id=id)
        serializer = solve_reconstruction_serializers.SolveSerializer(solve)
        return Response(serializer.data)


class SolveContestView(APIView):
    permission_classes = [SolveContestPermission]

    def get(self, request, contest_number, discipline):
        # return all scrambles and solves for scrambles if they already made

        contest = ContestModel.objects.get(contest_number=contest_number)
        scrambles = contest.scramble_set.filter(discipline__name=discipline).filter(solve_set__user=request.user.id)
        print(scrambles)

        serializer = solve_contest_serializers.ScrambleSerializer(scrambles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.query_params)


class OngoingContestNumberView(APIView):
    def get(self, request):
        ongoing_contest = ContestModel.objects.filter(ongoing=True).last()
        return Response(ongoing_contest.contest_number)
