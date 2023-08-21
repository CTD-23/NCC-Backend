# Generated by Django 4.2.2 on 2023-08-21 06:56

import datetime
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_team_islogin_alter_submission_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='team',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 21, 12, 26, 5, 227430)),
        ),
    ]
