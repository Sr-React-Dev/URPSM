# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0008_auto_20161101_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='model',
            name='stats',
        ),
        migrations.AddField(
            model_name='model',
            name='repaired_items',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='model',
            name='repairing_request',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='model',
            name='unlocked_items',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='model',
            name='unlocking_request',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Stat',
        ),
    ]
