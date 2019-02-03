# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0018_auto_20161101_1946'),
        ('notifications', '0002_auto_20161030_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='shop_order',
        ),
        migrations.AddField(
            model_name='notification',
            name='client',
            field=models.ForeignKey(related_name='client', blank=True, to='client.Client', null=True),
        ),
    ]
