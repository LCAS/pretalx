# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0014_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='contains_personal_data',
            field=models.BooleanField(default=True),
        ),
    ]
