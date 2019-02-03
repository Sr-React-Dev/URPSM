# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0020_auto_20170108_1746'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='endpoint',
        #     name='url',
        #     field=models.URLField(unique=True),
        # ),
        # migrations.AlterUniqueTogether(
        #     name='endpoint',
        #     unique_together=set([('url',)]),
        # ),
    ]
