# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0016_auto_20170721_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='completion_charges',
            field=models.CharField(default=None, max_length=4, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='logo',
            field=versatileimagefield.fields.VersatileImageField(default=b'icons/default_server.png', null=True, upload_to=b'server/%Y/%m/', blank=True),
        ),
    ]
