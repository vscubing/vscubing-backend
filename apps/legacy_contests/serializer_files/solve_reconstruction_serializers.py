from rest_framework import serializers

from ..models import SolveModel


class SolveSerializer(serializers.ModelSerializer):
    scramble = serializers.CharField(source='scramble.scramble')
    discipline = serializers.CharField(source='discipline.name')
    contest_number = serializers.IntegerField(source='contest.contest_number')
    username = serializers.CharField(source='user.username')
    scramble_position = serializers.CharField(source='scramble.position')
    dnf = serializers.BooleanField()

    class Meta:
        model = SolveModel
        fields = ['id', 'reconstruction', 'scramble', 'discipline', 'contest_number',
                  'username', 'scramble_position', 'dnf']
