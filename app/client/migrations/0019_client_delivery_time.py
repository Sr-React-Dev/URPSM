# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0018_auto_20161101_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='delivery_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
