# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20170611_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceCharges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge_text', models.CharField(max_length=50)),
                ('charge_amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('invoice', models.ForeignKey(to='shop.Invoices')),
            ],
        ),
    ]
