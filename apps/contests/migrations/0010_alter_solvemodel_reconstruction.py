# Generated by Django 4.2.6 on 2023-10-31 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0009_solvemodel_contest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvemodel',
            name='reconstruction',
            field=models.TextField(blank=True, max_length=15048, null=True),
        ),
    ]
