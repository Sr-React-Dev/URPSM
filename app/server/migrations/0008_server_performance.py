# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20161120_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='performance',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
