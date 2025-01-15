from django.contrib import admin

from .models import User, SettingsModel

admin.site.register(User)
admin.site.register(SettingsModel)
