from rest_framework.views import APIView, Response
from drf_spectacular.views import extend_schema


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListApi(APIView):
    def get(self, request):
        # selectors: select all solves including round_sessions` data to every solve and then sort on frontend
        # filters
        # serializers
        return Response(data={'json': 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class RoundSessionWithSolvesListApi(APIView):
    def get(self, request):
        # selectors: select needed round_session models with nested solves
        # filters
        # serializers
        return Response(data={'json': 'data'})
