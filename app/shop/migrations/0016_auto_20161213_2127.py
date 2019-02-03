# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_shop_performance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='logo',
            field=easy_thumbnails.fields.ThumbnailerImageField(default=b'icons/default_store.png', null=True, upload_to=b'shop/%Y/%m/', blank=True),
        ),
    ]
