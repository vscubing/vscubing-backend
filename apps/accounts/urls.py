from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .apis import GoogleLoginApi, UserRedirectApi, CurrentUserApi, ChangeUsernameApi


urlpatterns = [
    path("~redirect/", view=UserRedirectApi.as_view(), name="redirect"),
    path("google/login/", GoogleLoginApi.as_view(), name="google-login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('current-user/', CurrentUserApi.as_view(), name='current-user'),
    path('change-username/', ChangeUsernameApi.as_view(), name='change-username')
]
