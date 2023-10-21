from django.urls import path

from .views import GoogleLoginView, UserRedirectView, AUserView


urlpatterns = [
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path('current_user/', AUserView.as_view(), name='current_user')
]
