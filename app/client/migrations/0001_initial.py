# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import phonenumber_field.modelfields
from decimal import Decimal
import easy_thumbnails.fields
from django.conf import settings
import uuidfield.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
        ('phone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(default=0, max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('ref', models.CharField(default=90173732, unique=True, max_length=50)),
                ('serial', models.CharField(max_length=255)),
                ('imei', models.CharField(max_length=255)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(help_text=b'eg: +212612345678', max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('status', models.CharField(default=b'p', max_length=64, choices=[(b'p', b'Pending'), (b'c', b'Need Your Call'), (b'r', b'Ready')])),
                ('status_description', models.TextField(null=True, blank=True)),
                ('todo', models.CharField(default=b'r', max_length=64, choices=[(b'r', b'Repairing'), (b'f', b'Flashing'), (b'u', b'Unlocking')])),
                ('todo_description', models.TextField(null=True, blank=True)),
                ('paid', models.BooleanField(default=False)),
                ('delivered_at', models.DateTimeField()),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(to='phone.Brand')),
                ('model', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'brand', chained_field=b'brand', auto_choose=True, to='phone.Model')),
                ('paid_for', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('shop', models.ForeignKey(related_name='phone_shop', to='shop.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'phone/%Y/%m/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(related_name='images_phone', to='client.Client')),
            ],
        ),
        migrations.AddField(
            model_name='addon',
            name='client',
            field=models.ForeignKey(related_name='addons_phone', to='client.Client'),
        ),
        migrations.AlterUniqueTogether(
            name='addon',
            unique_together=set([('name', 'client')]),
        ),
    ]
