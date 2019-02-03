# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0011_model_satisfied_clients_count'),
        ('order', '0013_auto_20161125_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseorder',
            name='brand',
            field=models.ForeignKey(related_name='order_brand', default=None, blank=True, to='phone.Brand', null=True),
        ),
        migrations.AddField(
            model_name='baseorder',
            name='model',
            field=models.ForeignKey(related_name='order_model', default=None, blank=True, to='phone.Model', null=True),
        ),
    ]
