from django.urls import path

from .views import *


from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'contests', ContestViewSet, basename='contest')
router.register(r'disciplines', DisciplineViewSet, basename='discipline')
router.register(r'rounds_sessions', RoundSessionViewSet, basename='round_session')
router.register(r'solves', SolveViewSet, basename='solve')
router.register(r'scrambles', ScrambleViewSet, basename='scramble')
urlpatterns = router.urls
