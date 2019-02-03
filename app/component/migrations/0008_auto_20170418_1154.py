# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0007_auto_20151210_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(upload_to=b'components/%Y/%m/', blank=True),
        ),
    ]
