from django.urls import path

from .views import DashboardView, ContestView, SolveContestView, OngoingContestNumberView, SolveReconstructionSerializer, NewContestView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('contest/<int:contest_number>/<str:discipline>/', ContestView.as_view(), name='contest'),
    path('solve_contest/<int:contest_number>/<str:discipline>/', SolveContestView.as_view(), name='solve-contest'),
    path('ongoing_contest_number/', OngoingContestNumberView.as_view(), name='solve-contest'),
    path('solve_reconstruction/<int:id>/', SolveReconstructionSerializer.as_view(), name='solve-info'),
    path('new_contest/', NewContestView.as_view(), name='new-contest'),
]
