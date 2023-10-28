from rest_framework import serializers

from .models import ContestModel, DisciplineModel, SolveModel, RoundModel, ScrambleModel
from apps.accounts.models import User


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplineModel
        fields = '__all__'


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestModel
        fields = '__all__'


class ScrambleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundModel
        fields = '__all__'


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundModel
        fields = '__all__'


class SolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolveModel
        fields = '__all__'

