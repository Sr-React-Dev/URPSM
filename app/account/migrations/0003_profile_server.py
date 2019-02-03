# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
        ('account', '0002_profile_block_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='server',
            field=models.ForeignKey(related_name='user_server', blank=True, to='server.Server', null=True),
        ),
    ]
