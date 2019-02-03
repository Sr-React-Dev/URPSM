# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_auto_20151031_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='todo',
            field=models.CharField(default=b'r', max_length=64, choices=[(b'r', b'Repairing'), (b'f', b'Flashing'), (b'u', b'Unlocking'), (b'n', b"Can't Repaired")]),
        ),
    ]
