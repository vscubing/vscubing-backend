from django.urls import path

from .views import DashboardView, ContestView, SolveContestView, OngoingContestNumberView, SolveReconstructionSerializer

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('contest/<int:contest_number>/<str:discipline>/', ContestView.as_view(), name='past-contest'),
    path('solve_contest/<int:contest_number>/<str:discipline>/', SolveContestView.as_view(), name='solve-contest'),
    path('ongoing_contest_number/', OngoingContestNumberView.as_view(), name='solve-contest'),
    path('solve_info/<int:id>/', SolveReconstructionSerializer.as_view(), name='solve-info'),
]
