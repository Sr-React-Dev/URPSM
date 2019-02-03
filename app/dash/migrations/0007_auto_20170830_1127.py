# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0006_auto_20170822_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyvaluestore',
            name='value',
            field=models.TextField(blank=True),
        ),
    ]
