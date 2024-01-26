from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GoogleLoginView, UserRedirectView, CurrentUserView, ChangeUsernameView


urlpatterns = [
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("google/login/", GoogleLoginView.as_view(), name="google-login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('change-username/', ChangeUsernameView.as_view(), name='change-username')
]
