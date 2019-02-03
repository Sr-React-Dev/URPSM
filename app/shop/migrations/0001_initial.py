# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django_countries.fields
from decimal import Decimal
import easy_thumbnails.fields
import uuidfield.fields
import phonenumber_field.modelfields
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField(editable=False)),
                ('balance', models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('logo', easy_thumbnails.fields.ThumbnailerImageField(default=b'default.png', null=True, upload_to=b'shop/%Y/%m/', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('vat', models.PositiveIntegerField(default=0, help_text=b'VAT eg: 20')),
                ('shop_phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'eg: +212612345678', max_length=128)),
                ('shop_email', models.EmailField(max_length=254)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('address', models.CharField(max_length=300)),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('facebook', models.URLField(null=True, blank=True)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('google_plus', models.URLField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
