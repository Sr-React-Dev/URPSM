# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_invoices_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='admin_comments',
            field=models.TextField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='invoices',
            name='proof_upload_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='invoices',
            name='sec_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='invoices',
            name='method',
            field=models.CharField(max_length=30, choices=[(b'WESTERNUNION', b'WESTERNUNION'), (b'MONEYGRAM', b'MONEYGRAM'), (b'WAFACASH', b'WAFACASH'), (b'BANK', b'BANK')]),
        ),
        migrations.AlterField(
            model_name='invoices',
            name='status',
            field=models.CharField(default=b'UNPAID', max_length=10, choices=[(b'PAID', b'PAID'), (b'UNPAID', b'UNPAID'), (b'REUPLOAD', b'REUPLOAD')]),
        ),
    ]
