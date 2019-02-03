# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.antifraud.validators


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_baseorder_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseorder',
            name='imei',
            field=models.CharField(max_length=15, validators=[app.antifraud.validators.validate_imei]),
        ),
    ]
