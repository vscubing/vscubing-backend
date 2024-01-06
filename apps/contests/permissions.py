from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework.views import APIView, Response

from apps.accounts.models import User

from .models import ContestModel, RoundSessionModel


USER_NOT_VERIFIED_ERROR_MESSAGE = 'user is not verified, try to change your username'


class Vieew(APIView):
    def get(self, request):
        return Response(200)


def check_contest_exists(contest_number):
    try:
        return ContestModel.objects.get(contest_number=contest_number)
    except ObjectDoesNotExist:
        APIException.default_detail = "Contest does not exist"
        APIException.status_code = 404
        raise APIException


def api_exception_403(detail_message):
    APIException.status_code = 403
    APIException.default_detail = detail_message
    raise APIException


class ContestPermission(BasePermission):

    def has_permission(self, request, view):
        contest_number = view.kwargs.get('contest_number')
        discipline = view.kwargs.get('discipline')
        user = request.user

        contest = check_contest_exists(contest_number=contest_number)
        if not contest.ongoing:
            return True

        if not bool(user and user.is_authenticated):
            APIException.status_code = 401
            raise APIException

        if user.is_verified:

            round_session = RoundSessionModel.objects.filter(contest__contest_number=contest_number,
                                                             discipline__name=discipline,
                                                             submitted=True,
                                                             user=user.id)
            if not round_session:
                message = "User didn't solve ongoing contest"
                api_exception_403(message)
            return True
        else:
            api_exception_403(USER_NOT_VERIFIED_ERROR_MESSAGE)


class SolveContestPermission(BasePermission):
    def has_permission(self, request, view):
        contest_number = view.kwargs.get('contest_number')
        discipline = view.kwargs.get('discipline')
        user = request.user
        check_contest_exists(contest_number=contest_number)

        if not bool(user and user.is_authenticated):
            return False

        if user.is_verified:
            user = User.objects.get(id=user.id)
            round_session = user.round_session_set.filter(contest__contest_number=contest_number,
                                                          submitted=True,
                                                          discipline__name=discipline).last()
            if not round_session:
                return True
            message = "User solved contest already"
            api_exception_403(message)
        else:
            api_exception_403(USER_NOT_VERIFIED_ERROR_MESSAGE)
