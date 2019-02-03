# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20161125_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='performance',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
    ]
