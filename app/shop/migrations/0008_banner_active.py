# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20151223_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
