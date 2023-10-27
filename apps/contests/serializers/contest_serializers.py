from rest_framework import serializers

from ..models import SolveModel


class ContestSubmittedSolvesSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    discipline = serializers.CharField(source='discipline.name')
    scramble_position = serializers.CharField(source='scramble.position')

    class Meta:
        model = SolveModel
        fields = ['id', 'username', 'time_ms', 'discipline', 'scramble_position']

