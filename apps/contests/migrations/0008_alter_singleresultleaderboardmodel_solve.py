# Generated by Django 4.2.6 on 2024-06-19 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0007_singleresultleaderboardmodel_time_ms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleresultleaderboardmodel',
            name='solve',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='contests.solvemodel'),
        ),
    ]
