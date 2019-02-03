# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20161101_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseorder',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
