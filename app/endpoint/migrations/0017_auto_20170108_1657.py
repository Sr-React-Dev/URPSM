# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0016_auto_20170104_2142'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='endpoint',
        #     name='url',
        #     field=models.URLField(unique=True),
        # ),
        migrations.AlterField(
            model_name='network',
            name='name',
            field=models.CharField(max_length=255),
        ),
        # migrations.AlterField(
        #     model_name='network',
        #     name='services',
        #     field=django.contrib.postgres.fields.hstore.HStoreField(default={}),
        # ),
    ]
