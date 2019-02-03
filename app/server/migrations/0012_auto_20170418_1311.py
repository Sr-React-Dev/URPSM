# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_auto_20170418_1154'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='server',
        #     name='credit',
        #     field=models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])

        #     ),
           
    ]

