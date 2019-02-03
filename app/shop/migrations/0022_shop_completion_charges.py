# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_invoicecharges'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='completion_charges',
            field=models.CharField(default=None, max_length=4, null=True),
        ),
    ]
