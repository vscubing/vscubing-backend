import django_filters

from .models import (
    RoundSessionModel,
)


class RoundSessionFilter(django_filters.FilterSet):
    contest_id = django_filters.NumberFilter()
    discipline_id = django_filters.NumberFilter()

    class Meta:
        model = RoundSessionModel
        fields = ('discipline_id', 'contest_id')
