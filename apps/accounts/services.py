from .models import User
from rest_framework import exceptions
from apps.core.exceptions import ConflictException

from .models import SettingsModel


class UserService:
    def change_username(self, username, user_id):
        if User.objects.filter(username=username).exists():
            raise ConflictException("Username is already taken.")

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


class SettingsService:
    def __init__(self, user_id):
        self.user = User.objects.get(id=user_id)

    def update(self, cstimer_inspection_voice_alert, cstimer_animation_duration):
        settings = SettingsModel.objects.get(user=self.user)

        if cstimer_inspection_voice_alert is not None:
            settings.cstimer_inspection_voice_alert = cstimer_inspection_voice_alert

        if cstimer_animation_duration is not None:
            settings.cstimer_animation_duration = cstimer_animation_duration

        settings.save()
