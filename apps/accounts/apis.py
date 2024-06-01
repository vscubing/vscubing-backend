from os import getenv

from rest_framework.views import APIView, Response, status
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
from apps.core.utils import inline_serializer
from .services import UserService

GOOGLE_REDIRECT_URL = getenv('GOOGLE_REDIRECT_URL')


class GoogleLoginApi(SocialLoginView):
    class OutputSerializer(serializers.Serializer):
        access = serializers.CharField()
        refresh = serializers.CharField()
        user = inline_serializer(name='accounts.GoogleLoginUserSerializer', fields={
            'pk': serializers.IntegerField(),
            'email': serializers.CharField()
        })

        class Meta:
            ref_name = 'accounts.GoogleLoginOutputSerializer'

    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_REDIRECT_URL
    client_class = OAuth2Client

    @extend_schema(
        responses={200: OutputSerializer},
        parameters=[
            OpenApiParameter(
                name='code',
                location=OpenApiParameter.QUERY,
                description='code',
                required=True,
                type=str
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        # Call the post method of the parent class
        result = super().post(request, *args, **kwargs)

        # Add your custom logic here if needed

        return result


class UserRedirectApi(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return GOOGLE_REDIRECT_URL


class CurrentUserApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        username = serializers.CharField()
        auth_completed = serializers.BooleanField()

        class Meta:
            ref_name = 'accounts.CurrentUserOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
    )
    def get(self, request):
        data = {'username': request.user.username, 'auth_completed': request.user.is_verified}
        data = self.OutputSerializer(data).data
        return Response(data)


class ChangeUsernameApi(APIView):
    class ChangeUsernameInputSerializer(serializers.Serializer):
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
            ref_name = 'accounts.ChangeUsernameInputSerializer'

    @extend_schema(
        request=ChangeUsernameInputSerializer(),
    )
    def put(self, request):
        service = UserService()
        serializer = self.ChangeUsernameInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = service.change_username(**serializer.validated_data, user_id=request.user.id)
        return Response(status=status.HTTP_200_OK)
