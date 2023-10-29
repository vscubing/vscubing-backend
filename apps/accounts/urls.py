from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GoogleLoginView, UserRedirectView, AUserView


urlpatterns = [
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('current_user/', AUserView.as_view(), name='current_user'),
]
