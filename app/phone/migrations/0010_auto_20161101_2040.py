# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0009_auto_20161101_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='flashed_items',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='model',
            name='flashing_request',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
