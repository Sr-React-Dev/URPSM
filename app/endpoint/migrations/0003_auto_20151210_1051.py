# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0002_endpoint_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='active',
            field=models.BooleanField(default=False),
        )
    ]
