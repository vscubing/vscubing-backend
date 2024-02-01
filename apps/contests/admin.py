from django.contrib import admin

from .models import DisciplineModel, ScrambleModel, ContestModel, SolveModel, RoundSessionModel

admin.site.register([DisciplineModel, ScrambleModel, ContestModel, SolveModel, RoundSessionModel])
