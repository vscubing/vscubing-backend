from django.db import models

from apps.accounts.models import User
from apps.core.models import BaseModel


class ContestModel(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, db_index=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    is_ongoing = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class DisciplineModel(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True, db_index=True)

    def __str__(self):
        return self.name


class ScrambleModel(BaseModel):
    position = models.CharField(max_length=10)
    moves = models.TextField(max_length=512)
    is_extra = models.BooleanField(default=False)

    contest = models.ForeignKey(ContestModel, on_delete=models.CASCADE, related_name='scramble_set')
    discipline = models.ForeignKey(DisciplineModel, on_delete=models.CASCADE, related_name='scramble_set')

    def __str__(self):
        return self.moves


class RoundSessionModel(BaseModel):
    avg_ms = models.IntegerField(default=None, null=True, blank=True)
    is_dnf = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='round_session_set')
    contest = models.ForeignKey(ContestModel, on_delete=models.CASCADE, related_name='round_session_set')
    discipline = models.ForeignKey(DisciplineModel, on_delete=models.CASCADE, related_name='round_session_set')

    def __str__(self):
        return f"{self.user.username}, avg_ms {self.avg_ms}, id {self.pk}"


class SolveModel(BaseModel):
    time_ms = models.IntegerField(null=True, blank=True)
    is_dnf = models.BooleanField(default=False)
    extra_id = models.IntegerField(default=None, null=True, blank=True)
    SUBMITTED_STATE_CHOICES = [
        ('pending', 'pending'),
        ('submitted', 'submitted'),
        ('contest_submitted', 'contest_submitted'),
        ('changed_to_extra', 'changed_to_extra')
    ]
    submission_state = models.CharField(max_length=96, default='pending', choices=SUBMITTED_STATE_CHOICES)
    reconstruction = models.TextField(max_length=15048, null=True, blank=True)

    scramble = models.ForeignKey(ScrambleModel, on_delete=models.CASCADE, related_name='solve_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solve_set')
    discipline = models.ForeignKey(DisciplineModel, on_delete=models.CASCADE, related_name='solve_set')
    round_session = models.ForeignKey(RoundSessionModel, on_delete=models.CASCADE, related_name='solve_set')
    contest = models.ForeignKey(ContestModel, on_delete=models.CASCADE, related_name='solve_set')

    def __str__(self):
        return f"{self.user.username}, time_ms {self.time_ms}, id {self.pk}"


class SingleResultLeaderboardModel(models.Model):
    solve = models.OneToOneField(SolveModel, on_delete=models.CASCADE, unique=True)
    time_ms = models.IntegerField(db_index=True)

    def __str__(self):
        return f'{self.solve.user.username} {self.solve}'


class TnoodleScramblesModel(BaseModel):
    moves = models.CharField(max_length=150, unique=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.moves
