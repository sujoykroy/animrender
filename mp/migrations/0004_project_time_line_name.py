# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0003_auto_20171031_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='time_line_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
