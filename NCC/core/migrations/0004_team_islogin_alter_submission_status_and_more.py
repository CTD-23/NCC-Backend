# Generated by Django 4.2.2 on 2023-08-07 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_team_lastupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='isLogin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(blank=True, choices=[('TLE', 'Time Limit Exceeded'), ('MLE', 'Memory Limit Exceeded'), ('CE', 'Compilation Error'), ('RE', 'Runtime Error'), ('WA', 'Wrong Answer'), ('AC', 'Accepted'), ('PEN', 'Pending')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 7, 15, 26, 39, 587603)),
        ),
    ]