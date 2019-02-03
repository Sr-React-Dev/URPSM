# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0010_endpoint_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='network',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
    ]
