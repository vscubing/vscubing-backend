from rest_framework import serializers

from ..models import SolveModel, ScrambleModel


class SolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolveModel
        fields = ['reconstruction', 'time_ms', 'user']


class ScrambleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    scramble = serializers.CharField()
    extra = serializers.BooleanField()

    class Meta:
        model = ScrambleModel
        fields = ['scramble', 'extra', 'id']
