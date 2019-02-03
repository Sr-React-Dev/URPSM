# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_server_performance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='logo',
            field=easy_thumbnails.fields.ThumbnailerImageField(default=b'icons/default_server.png', null=True, upload_to=b'server/%Y/%m/', blank=True),
        ),
    ]
