from django.contrib import admin

from .models import DisciplineModel, ScrambleModel, ContestModel, SolveModel, RoundSessionModel, SingleResultLeaderboardModel

admin.site.register([DisciplineModel, ScrambleModel, ContestModel, SolveModel, RoundSessionModel, SingleResultLeaderboardModel])
