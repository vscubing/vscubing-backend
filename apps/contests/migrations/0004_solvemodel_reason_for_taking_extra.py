# Generated by Django 4.2.6 on 2025-03-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0003_tnoodlescramblesmodel_discipline'),
    ]

    operations = [
        migrations.AddField(
            model_name='solvemodel',
            name='reason_for_taking_extra',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
