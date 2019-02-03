# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0019_client_delivery_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='delivered_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
