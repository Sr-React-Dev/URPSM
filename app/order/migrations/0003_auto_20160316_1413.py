# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_network'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='emei',
            new_name='imei',
        ),
    ]
