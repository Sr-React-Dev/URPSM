# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_remove_baseorder_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseorder',
            name='amount',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
