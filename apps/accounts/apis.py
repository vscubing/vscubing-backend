from os import getenv
from random import choices

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
from urllib3 import request

from .serializers import UserSerializer
from .models import User, SettingsModel
from apps.core.utils import inline_serializer
from .services import UserService, SettingsService
from .selectors import SettingsSelector

GOOGLE_REDIRECT_URL = getenv('GOOGLE_REDIRECT_URL')


class GoogleLoginApi(SocialLoginView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()

        class Meta:
            ref_name = 'accounts.GoogleLoginInputSerializer'

    class OutputSerializer(serializers.Serializer):
        access = serializers.CharField()
        refresh = serializers.CharField()
        user = inline_serializer(fields={
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
        request=InputSerializer
    )
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
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
        id = serializers.IntegerField()
        username = serializers.CharField()
        email = serializers.EmailField()
        is_verified = serializers.BooleanField()

        class Meta:
            ref_name = 'accounts.CurrentUserOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()},
    )
    def get(self, request):
        data = request.user
        data = self.OutputSerializer(data).data
        return Response(data)


class ChangeUsernameApi(APIView):
    permission_classes = [IsAuthenticated]

    class ChangeUsernameInputSerializer(serializers.Serializer):
        username = serializers.CharField(
            max_length=20,
            min_length=3,
            validators=[RegexValidator(
                regex='^[a-zA-Z0-9_]*$',
                message='Username must be alphanumeric',
                code='invalid_username'
            )]
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


class SettingsRetrieveApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        cstimer_inspection_voice_alert = serializers.CharField()
        cstimer_animation_duration = serializers.IntegerField()
        cstimer_camera_position_theta = serializers.IntegerField()
        cstimer_camera_position_phi = serializers.IntegerField()

        class Meta:
            ref_name = 'accounts.SettingsUpdateOutputSerializer'

    @extend_schema(
        responses={200: OutputSerializer()}
    )
    def get(self, request):
        selector = SettingsSelector(user_id=request.user.id)
        data = selector.retrieve()
        data = self.OutputSerializer(data).data
        return Response(data)


class SettingsUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        cstimer_inspection_voice_alert = serializers.CharField(required=False)
        cstimer_animation_duration = serializers.IntegerField(required=False)
        cstimer_camera_position_theta = serializers.IntegerField(required=False)
        cstimer_camera_position_phi = serializers.IntegerField(required=False)

        class Meta:
            ref_name = 'accounts.SettingsUpdateInputSerializer'

    @extend_schema(
        request=InputSerializer(),
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = SettingsService(user_id=request.user.id)
        service.update(**serializer.validated_data)

        return Response(status=200)
