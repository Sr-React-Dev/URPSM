# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0003_model_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'phone/', blank=True),
        ),
    ]
