from django.contrib import admin

from .models import DisciplineModel, ScrambleModel, ContestModel, SolveModel

admin.site.register([DisciplineModel, ScrambleModel, ContestModel, SolveModel])
