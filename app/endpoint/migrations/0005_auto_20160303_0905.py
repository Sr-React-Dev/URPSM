# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0004_auto_20160303_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='network',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
