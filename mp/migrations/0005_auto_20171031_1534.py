# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0004_project_time_line_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segment',
            name='duration',
        ),
        migrations.AddField(
            model_name='segment',
            name='end_time',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='segment',
            name='start_time',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
