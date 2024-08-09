from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .general_services import current_contest_retrieve


class OwnRoundSessionDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

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
    )
    def delete(self, request):
        user_id = request.user.id
        contest = current_contest_retrieve()
        try:
            round_session = contest.round_session_set.get(user_id=user_id)
            round_session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
