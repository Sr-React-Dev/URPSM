# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0011_auto_20160314_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='service',
            field=models.TextField(null=True, blank=True),
        ),
    ]
