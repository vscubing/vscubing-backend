# Generated by Django 4.2.6 on 2025-02-12 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_contestmodel_discipline_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='tnoodlescramblesmodel',
            name='discipline',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='tnoodle_scramble_set', to='contests.disciplinemodel'),
        ),
    ]
