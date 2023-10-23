from django.urls import path

from .views import DashboardPageView, ContestPageView, SolveContestView, OngoingContestNumberView

urlpatterns = [
    path('dashboard_page/', DashboardPageView.as_view(), name='dashboard-page'),
    path('contest/<int:contest_number>/<str:discipline>/', ContestPageView.as_view(), name='past-contest-page'),
    path('solve_contest/<str:discipline>/', SolveContestView.as_view(), name='solve-contest-page'),
    path('ongoing_contest_number/', OngoingContestNumberView.as_view(), name='solve-contest-page'),
]
