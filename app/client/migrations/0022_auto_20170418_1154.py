# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0021_auto_20161213_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(upload_to=b'phone/%Y/%m/'),
        ),
    ]
