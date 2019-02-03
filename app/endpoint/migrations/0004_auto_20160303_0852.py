# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0003_auto_20151210_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='network',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(1, b'Morocco Network'), (2, b'France Network')]),
        ),
        migrations.AlterUniqueTogether(
            name='endpoint',
            unique_together=set([('url', 'network')]),
        ),
    ]
