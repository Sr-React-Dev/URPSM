# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0002_auto_20150823_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='picture',
            field=models.ImageField(default='', upload_to=b'phone/'),
            preserve_default=False,
        ),
    ]
