# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0005_auto_20160303_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='service',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
