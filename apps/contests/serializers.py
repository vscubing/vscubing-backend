from rest_framework import serializers

from .models import ContestModel, DisciplineModel, SolveModel, RoundSessionModel, ScrambleModel
from apps.accounts.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'username']


class RoundSessionSerializer(DynamicFieldsModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.get('fields')
        discipline_fields = kwargs.pop('discipline_fields', None)
        solve_set_fields = kwargs.pop('solve_set_fields', None)

        super().__init__(*args, **kwargs)
        if discipline_fields:
            self.fields['discipline'] = DisciplineSerializer(fields=discipline_fields)
        elif 'discipline' in fields:
            self.fields['discipline'] = DisciplineSerializer(fields=['name'])
        if solve_set_fields:
            self.fields['solve_set'] = SolveSerializer(fields=solve_set_fields, many=True)

    id = serializers.IntegerField()
    submitted = serializers.BooleanField(required=False)

    class Meta:
        model = RoundSessionModel
        fields = ['id', 'submitted', 'avg_ms']


class DisciplineSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)

    class Meta:
        model = DisciplineModel
        fields = ['id', 'name']


class ContestSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField()
    contest_number = serializers.IntegerField(required=False)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    ongoing = serializers.BooleanField(required=False)

    class Meta:
        model = RoundSessionModel
        fields = ['id', 'contest_number', 'start', 'end', 'ongoing']


class ScrambleSerializer(DynamicFieldsModelSerializer):

    id = serializers.IntegerField(required=False)
    position = serializers.CharField(max_length=10, required=False)
    scramble = serializers.CharField(max_length=512, required=False)
    extra = serializers.BooleanField(required=False)

    class Meta:
        model = RoundSessionModel
        fields = ['id', 'submitted', 'scramble', 'extra', 'position']


class SolveSerializer(DynamicFieldsModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.get('fields', None)
        scramble_fields = kwargs.pop('scramble_fields', None)
        discipline_fields = kwargs.pop('discipline_fields', None)
        round_session_fields = kwargs.pop('round_session_fields', None)
        user_fields = kwargs.pop('user_fields', None)

        super().__init__(*args, **kwargs)
        if scramble_fields:
            self.fields['scramble'] = ScrambleSerializer(fields=scramble_fields)
        elif 'scramble' in fields:
            self.fields['scramble'] = ScrambleSerializer(fields=['position'])
        if discipline_fields:
            self.fields['discipline'] = DisciplineSerializer(fields=discipline_fields)
        elif 'discipline' in fields:
            self.fields['discipline'] = DisciplineSerializer(fields=['name'])
        if round_session_fields:
            self.fields['round_session'] = RoundSessionSerializer(fields=round_session_fields)
        elif 'round_session' in fields:
            self.fields['round_session'] = RoundSessionSerializer(fields=['id'])
        if user_fields:
            self.fields['user'] = UserSerializer(fields=user_fields)
        elif 'user' in fields:
            self.fields['user'] = UserSerializer(fields=['username'])

    id = serializers.IntegerField()
    time_ms = serializers.IntegerField(required=False)
    dnf = serializers.BooleanField(required=False)
    extra_id = serializers.IntegerField(required=False)
    state = serializers.CharField(max_length=96, required=False)
    reconstruction = serializers.CharField(max_length=15048, required=False)

    contest_number = serializers.IntegerField(source='round_session.contest.contest_number')

    class Meta:
        model = SolveModel
        fields = ['id', 'time_ms', 'dnf', 'extra_id', 'state', 'reconstruction', 'contest_number']
