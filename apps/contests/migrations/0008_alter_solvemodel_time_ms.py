# Generated by Django 4.2.6 on 2023-10-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0007_roundsessionmodel_dnf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvemodel',
            name='time_ms',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
