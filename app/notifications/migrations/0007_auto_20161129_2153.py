# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('notifications', '0006_auto_20161129_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='payment',
            field=models.ForeignKey(related_name='notif_payment', blank=True, to='payment.ServerPaymentTransaction', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(related_name='notif_sender', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=1, choices=[(b'L', 'new review from client'), (b'C', 'new shop review'), (b'H', 'client has to review'), (b'T', 'new order'), (b'S', 'an order has been delivered'), (b'Y', 'an order has exceeded delivery time'), (b'D', 'order cancelling refused'), (b'E', 'new component'), (b'A', 'new ticket'), (b'I', 'admin has responded to your ticket'), (b'Z', 'server has responded to you ticket'), (b'W', 'payment transaction accepted'), (b'M', 'payment transaction declined'), (b'K', 'new brand added'), (b'B', 'new model added'), (b'J', 'admin notification'), (b'G', 'client status has been changed'), (b'H', 'client status has been paid')]),
        ),
        migrations.AlterField(
            model_name='notification',
            name='server_order',
            field=models.ForeignKey(related_name='notif_order', blank=True, to='order.ServerOrder', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='to_user',
            field=models.ForeignKey(related_name='notif_recepient', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
