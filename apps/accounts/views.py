from os import getenv

from rest_framework.views import APIView, Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator

from .serializers import UserSerializer
from .models import User

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


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        username = serializers.CharField()
        auth_completed = serializers.CharField()

        class Meta:
            ref_name = 'accounts.CurrentUserOutputSerializer'

    @extend_schema(
        responses={200: UserSerializer},
        request=OutputSerializer,
    )
    def get(self, request):
        data = {'username': request.user.username, 'auth_completed': request.user.is_verified}
        data = self.OutputSerializer(data).data
        return Response(data)


class ChangeUsernameView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        username = serializers.CharField(
            max_length=20,
            min_length=3,
            validators=[RegexValidator(
                regex='^[a-zA-Z0-9_]*$',
                message='Username must be alphanumeric',
                code='invalid_username'
            ), UniqueValidator(queryset=User.objects.all())]
        )

        class Meta:
            model = User
            ref_name = 'accounts.ChangeUsernameInputSerializer'
            fields = ['id', 'username']

    @extend_schema(
        responses={200: UserSerializer},
        request=InputSerializer,
    )
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        if request.user == user and not request.user.is_verified:
            user = UserSerializer(user, data=request.data)
            user.is_valid(raise_exception=True)
            user.save()
            return Response(user.data)

        else:
            APIException.default_detail = 'you dont have permission'
            APIException.status_code = 403
            raise APIException
