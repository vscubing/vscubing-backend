# Generated by Django 4.2.6 on 2024-12-30 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestmodel',
            name='discipline_set',
            field=models.ManyToManyField(to='contests.disciplinemodel'),
        ),
    ]
