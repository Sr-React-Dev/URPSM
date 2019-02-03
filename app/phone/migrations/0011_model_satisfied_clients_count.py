# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0010_auto_20161101_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='satisfied_clients_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
