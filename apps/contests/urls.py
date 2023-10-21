from django.urls import path

from .views import DashboardPageView

urlpatterns = [
    path('dashboard_page/', DashboardPageView.as_view(), name='dashboard-page')
]
