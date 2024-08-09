from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from .models import RoundSessionModel
from .general_services import current_contest_retrieve


class OwnRoundSessionDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_id = request.user.id
        contest = current_contest_retrieve()
        try:
            round_session = contest.round_session_set.get(user_id=user_id)
            round_session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
