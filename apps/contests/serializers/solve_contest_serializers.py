from rest_framework import serializers

from ..models import SolveModel, ScrambleModel


class ScrambleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    scramble = serializers.CharField()
    extra = serializers.BooleanField()

    class Meta:
        model = ScrambleModel
        fields = ['scramble', 'extra', 'id', 'position']


class SubmittedSolveSerializer(serializers.ModelSerializer):
    scramble = ScrambleSerializer()

    class Meta:
        model = SolveModel
        fields = ['id', 'time_ms', 'dnf', 'scramble',]


class CurrentSolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolveModel
        fields = ['id', 'time_ms']


class CurrentScrambleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrambleModel
        fields = ['id', 'scramble', 'extra', 'position']


class RegularSolveSerializer(serializers.ModelSerializer):
    contest_number = serializers.IntegerField(source='contest.contest_number')

    class Meta:
        model = SolveModel
        fields = ['reconstruction', "time_ms",]