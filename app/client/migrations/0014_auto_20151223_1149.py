# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0013_auto_20151223_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(default=b'p', max_length=64, choices=[(b'p', b'Pending'), (b'c', b'Need Your Call'), (b'r', b'Ready'), (b'n', b"Can't Repaired")]),
        ),
        migrations.AlterField(
            model_name='client',
            name='todo',
            field=models.CharField(default=b'r', max_length=64, choices=[(b'r', b'Repairing'), (b'f', b'Flashing'), (b'u', b'Unlocking')]),
        ),
    ]
