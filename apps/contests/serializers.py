from rest_framework import serializers

from .models import ContestModel, DisciplineModel, SolveModel, RoundSessionModel, ScrambleModel
from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer


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


class UserSerializer01(DynamicFieldsModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'username']


class RoundSessionSerializer01(DynamicFieldsModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.get('fields')
        discipline_fields = kwargs.pop('discipline_fields', None)
        solve_set_fields = kwargs.pop('solve_set_fields', None)
        user_fields = kwargs.pop('user_fields', None)

        super().__init__(*args, **kwargs)
        if discipline_fields:
            self.fields['discipline'] = DisciplineSerializer01(fields=discipline_fields)
        elif 'discipline' in fields:
            self.fields['discipline'] = DisciplineSerializer01(fields=['name'])
        if user_fields:
            self.fields['user'] = UserSerializer01(fields=user_fields)
        if solve_set_fields:
            self.fields['solve_set'] = SolveSerializer(fields=solve_set_fields, many=True)

    id = serializers.IntegerField()
    submitted = serializers.BooleanField(required=False)

    class Meta:
        model = RoundSessionModel
        fields = ['id', 'submitted', 'avg_ms']


class DisciplineSerializer01(DynamicFieldsModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)

    class Meta:
        model = DisciplineModel
        fields = ['id', 'name']


class ContestSerializer01(DynamicFieldsModelSerializer):
    id = serializers.IntegerField()
    contest_number = serializers.IntegerField(required=False)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    ongoing = serializers.BooleanField(required=False)

    class Meta:
        model = RoundSessionModel
        fields = ['id', 'contest_number', 'start', 'end', 'ongoing']


class ScrambleSerializer01(DynamicFieldsModelSerializer):

    id = serializers.IntegerField(required=False)
    position = serializers.CharField(max_length=10, required=False)
    scramble = serializers.CharField(max_length=512, required=False)
    extra = serializers.BooleanField(required=False)

    class Meta:
        model = RoundSessionModel
        fields = ['id', 'submitted', 'scramble', 'extra', 'position']


# Refactored serializers


class SolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolveModel
        fields = ['id', 'time_ms', 'dnf', 'state', 'reconstruction', 'created']


class ScrambleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrambleModel
        fields = '__all__'


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestModel
        fields = '__all__'


class RoundSessionSerializer():
    class Meta:
        model = RoundSessionModel
        fields = '__all__'


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplineModel
        fields = '__all__'


class SolveWithRelatedFieldsSerializer(SolveSerializer):
    contest = ContestSerializer()
    discipline = DisciplineSerializer()
    scramble = ScrambleSerializer()
    user = UserSerializer()

    class Meta(SolveSerializer.Meta):
        fields = SolveSerializer.Meta.fields + ['contest', 'discipline', 'scramble', 'user']
