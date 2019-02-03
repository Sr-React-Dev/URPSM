# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
from decimal import Decimal
import easy_thumbnails.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
        ('phone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'components/%Y/%m/')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(default=0, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('sold', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(to='phone.Brand')),
                ('model', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'brand', chained_field=b'brand', auto_choose=True, to='phone.Model')),
                ('shop', models.ForeignKey(related_name='component_shop', to='shop.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='component',
            name='type',
            field=models.ForeignKey(related_name='component_type', to='component.Type'),
        ),
    ]
