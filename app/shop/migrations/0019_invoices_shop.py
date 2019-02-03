# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20170606_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='shop',
            field=models.ForeignKey(blank=True, to='shop.Shop', null=True),
        ),
    ]
