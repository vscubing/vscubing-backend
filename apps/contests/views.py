import time

from rest_framework.views import APIView, Response

from .models import ContestModel, SolveModel
from .serializers.dashboard_serializers import ContestSerializer, BestSolvesSerializer


class DashboardPageView(APIView):
    def get(self, request):
        contests = ContestModel.objects.all()
        start_time = time.time()
        solves = SolveModel.objects.all()
        contests_serializer = ContestSerializer(contests, many=True)
        best_solves_serializer = BestSolvesSerializer(solves, many=True)
        print(time.time() - start_time)
        return Response({'contests': contests_serializer.data, 'best_solves': best_solves_serializer.data})
