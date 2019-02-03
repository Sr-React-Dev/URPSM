# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'banners/'),
        ),
    ]
