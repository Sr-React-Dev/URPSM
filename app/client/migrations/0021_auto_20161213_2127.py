# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.antifraud.validators


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0020_auto_20161128_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='imei',
            field=models.CharField(max_length=255, validators=[app.antifraud.validators.validate_imei]),
        ),
    ]
