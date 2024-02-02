from rest_framework.views import APIView, Response
from drf_spectacular.views import extend_schema
from rest_framework import serializers


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
class SolveRetrieveApi(APIView):
    def get(self, request, pk):
        # selectors: select one solve by id
        # filters: filter with filter serializer
        # serializers: serialize
        return Response(data={'json': 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListBestInDisciplineList(APIView):
    def get(self, request):
        return Response(data={'json', 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveListBestOfEveryUser(APIView):
    def get(self, request):
        return Response(data={'json', 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveCreateApi(APIView):
    def post(self, request):
        return Response(data={'json': 'data'})


@extend_schema(
    responses={200: {'json': 'data'}}
)
class SolveSubmitApi(APIView):
    def patch(self, request):
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


class ContestListApi(APIView):
    def get(self, request):
        return Response(data={'json': 'data'})



