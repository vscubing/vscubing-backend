# Generated by Django 4.2.6 on 2024-08-02 21:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0008_alter_singleresultleaderboardmodel_solve'),
    ]

    operations = [
        migrations.CreateModel(
            name='TnoodleScrambles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('moves', models.CharField(max_length=150, unique=True)),
                ('is_used', models.BooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='singleresultleaderboardmodel',
            name='solve',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contests.solvemodel'),
        ),
    ]
