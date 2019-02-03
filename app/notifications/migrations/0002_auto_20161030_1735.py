# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=1, choices=[(b'L', 'New review from client'), (b'D', 'Order cancelling refused'), (b'B', 'Order done'), (b'M', 'Abuse report confirmed'), (b'C', 'Repairing shop review request'), (b'F', 'Unlocking Server review request'), (b'A', 'New ticket'), (b'W', 'One order canceled'), (b'E', 'New component'), (b'S', 'Validate order cancelling'), (b'K', 'Abuse report declined'), (b'J', 'New client request'), (b'T', 'New order')]),
        ),
    ]
