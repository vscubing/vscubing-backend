import django_filters

from .models import (
    RoundSessionModel,
    ContestModel,
)


class RoundSessionFilter(django_filters.FilterSet):
    discipline_slug = django_filters.NumberFilter()
    order_by = django_filters.OrderingFilter(
        fields=(
            ('avg_ms', '-avg_ms')
        )
    )

    class Meta:
        model = RoundSessionModel
        fields = ('discipline_slug', 'order_by')


class ContestFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(
            ('created_at', '-created_at')
        )
    )
