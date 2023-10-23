from django.urls import path

from .views import DashboardPageView, ContestPageView

urlpatterns = [
    path('dashboard_page/', DashboardPageView.as_view(), name='dashboard-page'),
    path('contest_page/<int:contest_number>/<str:discipline>/', ContestPageView.as_view(), name='past-contest-page'),
]
