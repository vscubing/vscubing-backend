# Generated by Django 4.2.6 on 2024-11-16 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('is_ongoing', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DisciplineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(max_length=128, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoundSessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('avg_ms', models.IntegerField(blank=True, default=None, null=True)),
                ('is_dnf', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_session_set', to='contests.contestmodel')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_session_set', to='contests.disciplinemodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_session_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ScrambleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(max_length=10)),
                ('moves', models.TextField(max_length=512)),
                ('is_extra', models.BooleanField(default=False)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scramble_set', to='contests.contestmodel')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scramble_set', to='contests.disciplinemodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TnoodleScramblesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('moves', models.CharField(max_length=150, unique=True)),
                ('is_used', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolveModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time_ms', models.IntegerField(blank=True, null=True)),
                ('is_dnf', models.BooleanField(default=False)),
                ('extra_id', models.IntegerField(blank=True, default=None, null=True)),
                ('submission_state', models.CharField(choices=[('pending', 'pending'), ('submitted', 'submitted'), ('contest_submitted', 'contest_submitted'), ('changed_to_extra', 'changed_to_extra')], default='pending', max_length=96)),
                ('reconstruction', models.TextField(blank=True, max_length=15048, null=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.contestmodel')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.disciplinemodel')),
                ('round_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.roundsessionmodel')),
                ('scramble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.scramblemodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SingleResultLeaderboardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_ms', models.IntegerField(db_index=True)),
                ('solve', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contests.solvemodel')),
            ],
        ),
    ]
