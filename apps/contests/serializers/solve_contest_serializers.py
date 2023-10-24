from rest_framework import serializers

from ..models import SolveModel, ScrambleModel


class SolveSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolveModel
        fields = ['reconstruction', 'time_ms', 'user']


class GetSolveContestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    scramble = serializers.CharField()
    extra = serializers.BooleanField()
    solve_set = SolveSetSerializer(many=True)

    class Meta:
        model = ScrambleModel
        fields = ['scramble', 'extra', 'id', 'solve_set']
