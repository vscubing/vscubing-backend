from django.db import models
from apps.accounts.models import User


class ContestModel(models.Model):
    contest_number = models.IntegerField(unique=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    ongoing = models.BooleanField(default=True)

    def __str__(self):
        return str(self.contest_number)


class DisciplineModel(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ScrambleModel(models.Model):
    position = models.CharField(max_length=10)
    scramble = models.TextField(max_length=512)
    extra = models.BooleanField()
    contest = models.ForeignKey(ContestModel, on_delete=models.CASCADE, related_name='scramble_set')
    discipline = models.ForeignKey(DisciplineModel, on_delete=models.CASCADE, related_name='scramble_set')

    def __str__(self):
        return self.scramble


class RoundModel(models.Model):
    avg_ms = models.IntegerField()
    submitted = models.BooleanField(default=False)
    contest = models.ForeignKey(ContestModel, on_delete=models.CASCADE, related_name='round_set')
    discipline = models.ForeignKey(DisciplineModel, on_delete=models.CASCADE, related_name='round_set')


class SolveModel(models.Model):
    time_ms = models.IntegerField()
    dnf = models.BooleanField(default=False)
    extra_id = models.IntegerField(default=None, null=True, blank=True)
    state = models.CharField(max_length=96, default='pending')
    reconstruction = models.TextField(max_length=15048)
    scramble = models.ForeignKey(ScrambleModel, on_delete=models.CASCADE, related_name='solve_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solve_set')
    discipline = models.ForeignKey(DisciplineModel, on_delete=models.CASCADE, related_name='solve_set')
    round = models.ForeignKey(RoundModel, on_delete=models.CASCADE, related_name='solve_set')

    def __str__(self):
        return f"{self.time_ms}"
