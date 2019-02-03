# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '__first__'),
        ('endpoint', '0012_auto_20160314_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endpoint',
            name='shop',
        ),
        migrations.AddField(
            model_name='endpoint',
            name='server',
            field=models.ForeignKey(to='server.Server', null=True),
            # preserve_default=False,
        ),
    ]
