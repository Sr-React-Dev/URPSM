# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20161125_2306'),
        ('server', '0007_auto_20161120_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerPaymentTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('balance', models.DecimalField(default=0, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('payment_type', models.CharField(max_length=100, choices=[(b'DEBIT', b'DEBIT'), (b'CREDIT', b'CREDIT')])),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('server', models.ForeignKey(to='server.Server')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopPaymentTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('balance', models.DecimalField(default=0, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('payment_type', models.CharField(max_length=100, choices=[(b'DEBIT', b'DEBIT'), (b'CREDIT', b'CREDIT')])),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField()),
                ('shop', models.ForeignKey(to='shop.Shop')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
