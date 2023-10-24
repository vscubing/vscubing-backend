from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist

from config import SOLVE_CONTEST_SUBMITTED_STATE
from .models import ContestModel, DisciplineModel, SolveModel, ScrambleModel
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
                user = User.objects.get(id=request.user.id)
                last_this_contest_solve = user.solve_set.filter(contest__contest_number=contest_number,
                                                                state=SOLVE_CONTEST_SUBMITTED_STATE,
                                                                discipline__name=discipline).last()
                if last_this_contest_solve:
                    return True
                elif not last_this_contest_solve:
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
        if bool(request.user and request.user.is_authenticated):
            return True
        else:
            return False
