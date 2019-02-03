# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20160924_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverorder',
            name='cancellation_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='serverorder',
            name='refund_amount',
            field=models.DecimalField(default=b'0', max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='serverorder',
            name='status',
            field=models.CharField(default=b'COMPLETED', max_length=255, choices=[(b'PENDING', b'PENDING'), (b'DELIVERED', b'DELIVERED'), (b'REJECTED', b'REJECTED'), (b'CANCELLED', b'CANCELLED'), (b'COMPLETED', b'COMPLETED'), (b'HOLD', b'HOLD')]),
        ),
        migrations.AddField(
            model_name='serverorder',
            name='urpsm_charge',
            field=models.DecimalField(default=b'0', max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='serverorder',
            name='urpsm_charge_factor',
            field=models.DecimalField(default=b'0', max_digits=12, decimal_places=2),
        ),
    ]
