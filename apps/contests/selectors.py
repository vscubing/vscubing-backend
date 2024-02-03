from .models import (
    RoundSessionModel,
)
from .filters import (
    RoundSessionFilter
)


class RoundSessionSelector:

    def list_with_solves(self, filters=None):
        filters = filters or {}
        # TODO add prefetch_related & select_related
        round_session_set = RoundSessionModel.objects.all()

        return RoundSessionFilter(filters, round_session_set).qs
