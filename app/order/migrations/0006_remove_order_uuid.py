# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='uuid',
        ),
    ]
