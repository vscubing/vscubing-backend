from rest_framework import serializers

from ..models import SolveModel


class SolveSerializer(serializers.ModelSerializer):
    scramble = serializers.CharField(source='scramble.scramble')

    class Meta:
        model = SolveModel
        fields = ['id', 'reconstruction', 'scramble']
