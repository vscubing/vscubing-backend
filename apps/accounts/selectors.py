from dataclasses import dataclass
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404

from .models import (
    SettingsModel,
    User,
)


class SettingsSelector:
    def __init__(self, user_id):
        self.user = User.objects.get(id=user_id)

    def retrieve(self):
        data = SettingsModel.objects.get(user=self.user)
        return data
