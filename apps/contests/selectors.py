from .models import (
    RoundSessionModel,
)


class RoundSessionSelector:

    def list_with_solves(self, params):
        round_session_set = RoundSessionModel.objects.all()
        return round_session_set
