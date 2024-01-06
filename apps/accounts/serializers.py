from django.core.validators import RegexValidator

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'username']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.is_verified = True
        instance.save()
        return instance
