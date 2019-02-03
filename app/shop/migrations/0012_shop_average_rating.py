# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20161028_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='average_rating',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
