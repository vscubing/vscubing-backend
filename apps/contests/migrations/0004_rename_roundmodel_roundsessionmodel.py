# Generated by Django 4.2.6 on 2023-10-28 09:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contests', '0003_alter_roundmodel_avg_ms'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RoundModel',
            new_name='RoundSessionModel',
        ),
    ]
