# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0009_auto_20160310_1549'),
        ('shop', '0008_banner_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(max_length=32)),
                ('ref', models.CharField(max_length=255)),
                ('emei', models.CharField(max_length=15)),
                ('amount', models.CharField(max_length=50)),
                ('network', models.CharField(max_length=255)),
                ('service', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('endpoint', models.ForeignKey(to='endpoint.Endpoint')),
                ('shop', models.ForeignKey(to='shop.Shop')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
    ]
