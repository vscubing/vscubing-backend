from rest_framework import serializers

from ..models import ContestModel, SolveModel, ScrambleModel
from apps.accounts.models import User


class ContestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContestModel
        fields = '__all__'


class ScrambleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrambleModel
        fields = ['scramble']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class BestSolvesSerializer(serializers.ModelSerializer):
    scramble = ScrambleSerializer()
    user = UserSerializer()

    class Meta:
        model = SolveModel
        fields = ['reconstruction', 'time_ms', 'scramble', 'user', 'contest']
