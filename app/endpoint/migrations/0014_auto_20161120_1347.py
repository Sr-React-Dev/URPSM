# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0013_auto_20160924_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='server',
            field=models.ForeignKey(related_name='server_endpoint', to='server.Server', null=True),
        ),
    ]
