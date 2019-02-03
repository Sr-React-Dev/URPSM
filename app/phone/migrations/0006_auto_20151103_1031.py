# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0005_brand_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=easy_thumbnails.fields.ThumbnailerImageField(null=True, upload_to=b'brand/', blank=True),
        ),
    ]
