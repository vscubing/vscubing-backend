from model_bakery import baker
# import factory
import json
import pytest

from apps.contests.models import ContestModel, SolveModel, DisciplineModel, ScrambleModel, RoundSessionModel

pytestmark = pytest.mark.django_db


class TestEndpoints:
    endpoint = '/api/contests/dashboard/'

    def test_dashboard(self, api_client):
        baker.make()
