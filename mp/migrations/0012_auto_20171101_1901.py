# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0011_project_extras'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='extras',
            field=models.TextField(default='{}'),
        ),
    ]