from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from .models import DisciplineModel
from .tasks import create_contest

from .general_services import current_contest_retrieve, generate_contest_service


class OwnRoundSessionDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        discipline_slug = serializers.CharField(required=False)

    @extend_schema(
        responses={
            204: None,  # No content
            400: None,  # No content
            401: OpenApiResponse(
                examples=[
                    OpenApiExample(
                        'Unauthorized',
                        value={
                            'detail': 'Authentication credentials were not provided.'
                        },
                        response_only=True,
                        status_codes=['401']
                    )
                ],
                response=OpenApiTypes.OBJECT
            )
        },
        request=InputSerializer(),
        parameters=[
            OpenApiParameter(
                name='discipline_slug',
                location=OpenApiParameter.QUERY,
                description='discipline slug',
                required=True,
                type=str,
            )
        ]
    )
    def delete(self, request):
        discipline_slug = request.query_params.get('discipline_slug')

        discipline = DisciplineModel.objects.get(slug=discipline_slug)
        user_id = request.user.id
        contest = current_contest_retrieve()
        try:
            round_session = contest.round_session_set.get(user_id=user_id, discipline=discipline)
            round_session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class NewContestCreateApi(APIView):
    @extend_schema(
        responses={
            201: None
        }
    )
    def post(self, request):
        create_contest()
        return Response(status=status.HTTP_201_CREATED)

