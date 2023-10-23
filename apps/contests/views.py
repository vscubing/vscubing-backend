import time

from rest_framework.views import APIView, Response

from apps.accounts.models import User
from .models import ContestModel, SolveModel, DisciplineModel
from .serializers import dashboard_serializers, contest_serializers


class DashboardPageView(APIView):
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


class ContestPageView(APIView):
    def get(self, request, contest_number, discipline):
        contest = ContestModel.objects.get(contest_number=contest_number)
        if not contest.ongoing:
            solves = contest.solve_set.filter(state='submitted', discipline__name=discipline).order_by('user_id', 'time_ms')
            serializer = contest_serializers.ContestSubmittedSolvesSerializer(solves, many=True)
            return Response(serializer.data)
        elif contest.ongoing:
            # need to check if state == "contest_submitted" to allow or not allow see ongoing contest
            user = User.objects.get(id=request.user.id)
            last_solve = user.solve_set.filter(discipline__name=discipline).order_by('id').last()
            print(last_solve.state)
            return Response(200)


class SolveContestView(APIView):
    def get(self, request):
        pass
