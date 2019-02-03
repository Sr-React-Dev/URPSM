# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ureview', '0006_auto_20161125_2306'),
        ('notifications', '0007_auto_20161129_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='server_review',
            field=models.ForeignKey(related_name='notif_server_review', blank=True, to='ureview.ServerReview', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='shop_review',
            field=models.ForeignKey(related_name='notif_shop_review', blank=True, to='ureview.ShopReview', null=True),
        ),
    ]
