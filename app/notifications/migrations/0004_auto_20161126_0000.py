# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20161110_1727'),
        ('notifications', '0003_auto_20161125_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='ticket',
            field=models.ForeignKey(related_name='notif_ticket', blank=True, to='ticket.OrderTicket', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='client',
            field=models.ForeignKey(related_name='notif_client', blank=True, to='client.Client', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='server',
            field=models.ForeignKey(related_name='notif_server', blank=True, to='server.Server', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='shop',
            field=models.ForeignKey(related_name='notif_shop', blank=True, to='shop.Shop', null=True),
        ),
    ]
