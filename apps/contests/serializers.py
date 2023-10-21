from rest_framework import serializers

from .models import ContestModel


class ContestSerializer(serializers.Serializer):
    name = serializers.IntegerField()
