# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_actionhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='BitcoinHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=60)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(null=True)),
                ('txhash', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(default=b'UNPAID', max_length=10)),
                ('invoice', models.ForeignKey(to='shop.Invoices')),
            ],
        ),
        migrations.CreateModel(
            name='BitcoinKeyInvoiceDict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=60)),
                ('index', models.CharField(max_length=5)),
                ('invoice', models.ForeignKey(to='shop.Invoices')),
            ],
        ),
        migrations.AddField(
            model_name='bitcoinhistory',
            name='key',
            field=models.ForeignKey(to='shop.BitcoinKeyInvoiceDict', null=True),
        ),
    ]
