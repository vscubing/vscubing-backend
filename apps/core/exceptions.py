from rest_framework.exceptions import APIException
from rest_framework import status


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Conflict occurred'


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request'


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found'
    default_code = 'not_found'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = {"detail": detail}
        else:
            self.detail = {"detail": self.default_detail}
