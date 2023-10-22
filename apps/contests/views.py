import time

from rest_framework.views import APIView, Response

from .models import ContestModel, SolveModel, DisciplineModel
from .serializers.dashboard_serializers import ContestSerializer, BestSolvesSerializer


class DashboardPageView(APIView):
    def get(self, request):
        contests = ContestModel.objects.all()
        disciplines = DisciplineModel.objects.all()

        solve_set = []
        for discipline in disciplines:
            solve = discipline.solve_set.order_by('time_ms').first()
            if solve:
                solve_set.append(solve)

        contests_serializer = ContestSerializer(contests, many=True)
        best_solves_serializer = BestSolvesSerializer(solve_set, many=True)
        return Response({'contests': contests_serializer.data, 'best_solves': best_solves_serializer.data})


class PastContestPage(APIView):
    def get(self, request):
        pass
