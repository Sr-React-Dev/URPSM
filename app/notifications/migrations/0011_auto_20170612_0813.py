# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20170611_1412'),
        ('notifications', '0010_auto_20161205_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='invoice',
            field=models.ForeignKey(related_name='notif_invoice', blank=True, to='shop.Invoices', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=1, choices=[(b'L', 'new review from client'), (b'C', 'new shop review'), (b'H', 'client has to review'), (b'T', 'new order'), (b'S', 'an order has been delivered'), (b'Y', 'an order has exceeded delivery time'), (b'D', 'order cancelling refused'), (b'E', 'new component'), (b'A', 'new ticket'), (b'I', 'admin has responded to your ticket'), (b'Z', 'server has responded to you ticket'), (b'Q', 'your did not respond to ticket within 3 days, order will be canceled'), (b'N', 'unlocking server did not respond to your ticket within 3 days, you will be refunded.'), (b'W', 'payment transaction accepted'), (b'M', 'payment transaction declined'), (b'K', 'new brand added'), (b'B', 'new model added'), (b'J', 'admin notification'), (b'G', 'client status has been changed'), (b'P', 'client status has been paid'), (b'P', 'proof was rejected. please re-upload'), (b'F', 'proof verified. funds added to account')]),
        ),
    ]
