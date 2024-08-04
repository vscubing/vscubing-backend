from django.apps import AppConfig


class ContestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contests'

    def ready(self):
        from .scheduler import start
        start()
