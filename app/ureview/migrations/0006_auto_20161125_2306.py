# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20161125_2306'),
        ('client', '0018_auto_20161101_1946'),
        ('ureview', '0005_auto_20161112_2109'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='serverreview',
        #     name='shop',
        #     field=models.ForeignKey(related_name='shop_review', default=False, to='shop.Shop'),
        # ),
        # migrations.AddField(
        #     model_name='shopreview',
        #     name='client',
        #     field=models.ForeignKey(related_name='client_review', default=False, to='client.Client'),
        # ),
    ]
