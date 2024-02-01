from rest_framework.views import APIView, Response
from drf_spectacular.views import extend_schema


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListApi(APIView):
    def get(self, request):
        # filter
        # serialize
        return Response(data={'json': 'data'})
