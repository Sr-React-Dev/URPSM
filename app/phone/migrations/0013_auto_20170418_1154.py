# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0012_auto_20161213_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=versatileimagefield.fields.VersatileImageField(null=True, upload_to=b'brand/', blank=True),
        ),
        migrations.AlterField(
            model_name='model',
            name='picture',
            field=versatileimagefield.fields.VersatileImageField(default=b'icons/default_phone.png', null=True, upload_to=b'phone/', blank=True),
        ),
    ]
