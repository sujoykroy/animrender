# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0012_auto_20171101_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
