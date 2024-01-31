# Generated by Django 4.2.6 on 2024-01-31 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('contest_number', models.IntegerField(unique=True)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(null=True)),
                ('ongoing', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DisciplineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='RoundSessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_ms', models.IntegerField(blank=True, default=None, null=True)),
                ('dnf', models.BooleanField(default=False)),
                ('submitted', models.BooleanField(default=False)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_session_set', to='contests.contestmodel')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_session_set', to='contests.disciplinemodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_session_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScrambleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=10)),
                ('scramble', models.TextField(max_length=512)),
                ('extra', models.BooleanField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scramble_set', to='contests.contestmodel')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scramble_set', to='contests.disciplinemodel')),
            ],
        ),
        migrations.CreateModel(
            name='SolveModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_ms', models.IntegerField(blank=True, null=True)),
                ('dnf', models.BooleanField(default=False)),
                ('extra_id', models.IntegerField(blank=True, default=None, null=True)),
                ('state', models.CharField(default='pending', max_length=96)),
                ('reconstruction', models.TextField(blank=True, max_length=15048, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.contestmodel')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.disciplinemodel')),
                ('round_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.roundsessionmodel')),
                ('scramble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to='contests.scramblemodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solve_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
