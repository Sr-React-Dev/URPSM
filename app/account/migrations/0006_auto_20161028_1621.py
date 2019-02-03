# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20161002_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_business',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='has_to_review',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_business_info_done',
            field=models.BooleanField(default=False),
        ),
    ]
