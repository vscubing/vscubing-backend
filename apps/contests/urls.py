from django.urls import path

from .views import *


from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'contests', ContestViewSet, basename='contest')
router.register(r'disciplines', DisciplineViewSet, basename='discipline')
router.register(r'round_sessions', RoundSessionViewSet, basename='round_session')
router.register(r'solves', SolveViewSet, basename='solve')
router.register(r'scrambles', ScrambleViewSet, basename='scramble')
urlpatterns = router.urls


false_urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('leaderboard/<str:discipline>/', LeaderboardView.as_view(), name='leaderboard'),
    path('contest/<int:contest_number>/discipline/<str:discipline>/', ContestView.as_view(), name='contest'),
    path('solve-contest/<int:contest_number>/discipline/<str:discipline>/', SolveContestView.as_view(), name='solve-contest'),
    path('ongoing-contest-number/', OngoingContestNumberView.as_view(), name='solve-contest'),
    path('solve-reconstruction/<int:id>/', SolveReconstructionSerializer.as_view(), name='solve-info'),
    path('new-contest/', NewContestView.as_view(), name='new-contest'),
    path('solve/', SolveView.as_view(), name='solve'),
    path('round-session/', RoundSessionView.as_view(), name='round-session')
]
