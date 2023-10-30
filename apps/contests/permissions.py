from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist

from config import SOLVE_CONTEST_SUBMITTED_STATE, SOLVE_SUBMITTED_STATE
from .models import ContestModel, DisciplineModel, SolveModel, ScrambleModel, RoundSessionModel
from apps.accounts.models import User
from rest_framework.views import APIView, Response


class Vieew(APIView):
    def get(self, request):
        return Response(200)


class ContestPermission(BasePermission):

    def has_permission(self, request, view):
        contest_number = view.kwargs.get('contest_number')
        discipline = view.kwargs.get('discipline')
        try:
            contest = ContestModel.objects.get(contest_number=contest_number)
        except ObjectDoesNotExist:
            APIException.default_detail = "Contest does not exist"
            APIException.status_code = 404
            raise APIException
        if contest.ongoing:
            if bool(request.user and request.user.is_authenticated):
                round_session = RoundSessionModel.objects.filter(contest__contest_number=contest_number,
                                                                 discipline__name=discipline, submitted=True)
                if round_session:
                    return True
                elif not round_session:
                    APIException.default_detail = "User didn't solve ongoing contest"
                    APIException.status_code = 403
                    raise APIException
            else:
                APIException.status_code = 401
                raise APIException

        elif not contest.ongoing:
            return True


class SolveContestPermission(BasePermission):
    def has_permission(self, request, view):
        contest_number = view.kwargs.get('contest_number')
        discipline = view.kwargs.get('discipline')
        try:
            contest = ContestModel.objects.get(contest_number=contest_number)
        except ObjectDoesNotExist:
            APIException.default_detail = "Contest does not exist"
            APIException.status_code = 404
            raise APIException

        if bool(request.user and request.user.is_authenticated):
            user = User.objects.get(id=request.user.id)
            round_session = user.round_session_set.filter(contest__contest_number=contest_number,
                                                                         submitted=True,
                                                                         discipline__name=discipline).last()
            if not round_session:
                return True
            elif round_session:
                APIException.default_detail = "User solved contest already"
                APIException.status_code = 403
                raise APIException
        else:
            return False
