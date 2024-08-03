from django.contrib import admin

from .models import (
    DisciplineModel,
    ScrambleModel,
    ContestModel,
    SolveModel,
    RoundSessionModel,
    SingleResultLeaderboardModel,
    TnoodleScramblesModel
)

admin.site.register([DisciplineModel, ScrambleModel, ContestModel, SolveModel,
                     RoundSessionModel, SingleResultLeaderboardModel, TnoodleScramblesModel])
