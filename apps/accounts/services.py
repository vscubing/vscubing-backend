from .models import User
from rest_framework import exceptions


class UserService:
    def change_username(self, username, user_id):
        user = User.objects.get(id=user_id)
        if user and not user.is_verified:
            user.username = username
            user.is_verified = True
            user.save()
            return user
        elif user.is_verified:
            raise exceptions.NotFound()
        elif not user:
            raise exceptions.NotFound()

        # else:
        #     APIException.default_detail = 'you dont have permission'
        #     APIException.status_code = 403
        #     raise APIException
