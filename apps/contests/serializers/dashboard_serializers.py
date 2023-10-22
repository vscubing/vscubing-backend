from rest_framework import serializers

from ..models import ContestModel, SolveModel, ScrambleModel, DisciplineModel
from apps.accounts.models import User


class ContestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContestModel
        fields = '__all__'


class BestSolvesSerializer(serializers.ModelSerializer):
    scramble = serializers.CharField(source='scramble.scramble')
    username = serializers.CharField(source='user.username')
    discipline = serializers.CharField(source='discipline.name')

    class Meta:
        model = SolveModel
        fields = ['reconstruction', 'time_ms', 'scramble', 'username', 'contest', 'discipline']

