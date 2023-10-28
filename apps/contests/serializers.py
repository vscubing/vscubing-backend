from rest_framework import serializers

from .models import ContestModel, DisciplineModel, SolveModel, RoundSessionModel, ScrambleModel
from apps.accounts.models import User


class DisciplineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)


class ContestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    contest_number = serializers.IntegerField(required=False)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    ongoing = serializers.BooleanField(required=False)


class ScrambleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    position = serializers.CharField(max_length=10, required=False)
    scramble = serializers.CharField(max_length=512, required=False)
    extra = serializers.BooleanField(required=False)
    contest = serializers.IntegerField(source='contest__contest_number', required=False)
    discipline = serializers.CharField(source='discipline__name', required=False)


class RoundSessionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    submitted = serializers.BooleanField(required=False)
    contest = serializers.IntegerField(source='contest__contest_number', required=False)
    discipline = serializers.CharField(source='discipline__name', required=False)


class SolveSerializer(serializers.Serializer):
    scramble = ScrambleSerializer(required=False)

    id = serializers.IntegerField()
    time_ms = serializers.IntegerField(required=False)
    dnf = serializers.BooleanField(required=False)
    extra_id = serializers.IntegerField(required=False)
    state = serializers.CharField(max_length=96, required=False)
    reconstruction = serializers.CharField(max_length=15048, required=False)

    contest = serializers.IntegerField(source='contest__contest_number', required=False)
    discipline = serializers.CharField(source='discipline__name', required=False)
    scramble = serializers.CharField(source='scramble__scramble', required=False)
    round = serializers.IntegerField(source='round__id', required=False)
