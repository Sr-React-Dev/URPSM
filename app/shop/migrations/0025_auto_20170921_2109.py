# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20170823_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='cancellation_charges',
            field=models.CharField(default=None, max_length=4, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='invoices',
            name='method',
            field=models.CharField(max_length=30, choices=[(b'WESTERNUNION', b'WESTERNUNION'), (b'MONEYGRAM', b'MONEYGRAM'), (b'WAFACASH', b'WAFACASH'), (b'BANK', b'BANK'), (b'BITCOIN', b'BITCOIN')]),
        ),
        migrations.AlterField(
            model_name='shop',
            name='completion_charges',
            field=models.CharField(default=None, max_length=4, null=True, blank=True),
        ),
    ]
