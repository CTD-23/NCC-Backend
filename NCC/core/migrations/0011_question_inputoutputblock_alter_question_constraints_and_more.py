# Generated by Django 4.2.2 on 2023-08-21 14:16

import datetime
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_team_lastupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='inputOutputBlock',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='constraints',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='ipFormate',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='opFormate',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='team',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 21, 19, 46, 46, 935215)),
        ),
    ]
