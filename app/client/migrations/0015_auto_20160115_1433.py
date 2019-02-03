# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0014_auto_20151223_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='addon',
            name='original_price',
            field=models.DecimalField(default=0, help_text=b'Addon original price.', max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='addon',
            name='price',
            field=models.DecimalField(default=0, help_text=b'Addon selling price.', max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
