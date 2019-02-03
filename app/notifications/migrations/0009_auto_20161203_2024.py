# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_auto_20161129_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=1, choices=[(b'L', 'new review from client'), (b'C', 'new shop review'), (b'H', 'client has to review'), (b'T', 'new order'), (b'S', 'an order has been delivered'), (b'Y', 'an order has exceeded delivery time'), (b'D', 'order cancelling refused'), (b'E', 'new component'), (b'A', 'new ticket'), (b'I', 'admin has responded to your ticket'), (b'Z', 'server has responded to you ticket'), (b'W', 'payment transaction accepted'), (b'M', 'payment transaction declined'), (b'K', 'new brand added'), (b'B', 'new model added'), (b'J', 'admin notification'), (b'G', 'client status has been changed'), (b'P', 'client status has been paid')]),
        ),
    ]
