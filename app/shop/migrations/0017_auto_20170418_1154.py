# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20161213_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner',
            field=versatileimagefield.fields.VersatileImageField(upload_to=b'banners/'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='logo',
            field=versatileimagefield.fields.VersatileImageField(default=b'icons/default_store.png', null=True, upload_to=b'shop/%Y/%m/', blank=True),
        ),
    ]
