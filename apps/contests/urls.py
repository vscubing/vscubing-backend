from django.urls import path

from .views import DashboardPageView, PastContestPage

urlpatterns = [
    path('dashboard_page/', DashboardPageView.as_view(), name='dashboard-page'),
    path('past_contest_page/<int:name>/<str:discipline>/', PastContestPage.as_view(), name='past-contest-page'),
]
