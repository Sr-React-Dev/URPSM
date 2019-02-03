# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0013_auto_20170418_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerSales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=30, choices=[(b'upcoming_payments', b'upcoming_payments'), (b'available_withdraw', b'available_withdraw'), (b'already_withdrawn', b'already_withdrawn'), (b'amount_completed', b'amount_completed')])),
                ('value', models.DecimalField(max_digits=9, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('server', models.ForeignKey(to='server.Server')),
            ],
        ),
    ]
