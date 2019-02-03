# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20161030_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverorder',
            name='server',
            field=models.ForeignKey(related_name='server_order', to='server.Server'),
        ),
        migrations.AlterField(
            model_name='serverorder',
            name='shop',
            field=models.ForeignKey(related_name='shop_server_order', to='shop.Shop'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='shop',
            field=models.ForeignKey(related_name='client_server_order', to='shop.Shop'),
        ),
    ]
