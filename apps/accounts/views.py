from os import getenv

from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

from scripts.fake_data import create_contest

GOOGLE_REDIRECT_URL = getenv('GOOGLE_REDIRECT_URL')


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_REDIRECT_URL
    client_class = OAuth2Client


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return GOOGLE_REDIRECT_URL


class AUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(f'{request.user.username}')
