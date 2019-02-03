# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('launch', '0002_auto_20160629_0158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='launchrock',
            name='name',
        ),
        migrations.AddField(
            model_name='launchrock',
            name='notify_him',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='launchrock',
            name='username',
            field=models.CharField(default=b'user', max_length=255, null=True, blank=True),
        ),
    ]
