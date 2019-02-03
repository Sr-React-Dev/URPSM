# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0019_auto_20170108_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='networks',
            field=models.ManyToManyField(default=None, to='endpoint.Network', blank=True),
        ),
    ]
