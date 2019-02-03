# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0015_auto_20160115_1433'),
        ('endpoint', '0013_auto_20160924_1836'),
        # ('shop', '0010_shop_is_server'),
        ('server', '__first__'),
        ('order', '0007_auto_20160413_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(max_length=255)),
                ('imei', models.CharField(max_length=15)),
                ('amount', models.CharField(default=b'0', max_length=50)),
                ('paid', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('delivery_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='endpoint',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shop',
        ),
        migrations.CreateModel(
            name='ServerOrder',
            fields=[
                ('baseorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.BaseOrder')),
                ('service', models.CharField(max_length=255)),
                ('endpoint', models.ForeignKey(to='endpoint.Endpoint')),
                ('server', models.ForeignKey(to='server.Server')),
                ('shop', models.ForeignKey(to='shop.Shop')),
            ],
            options={
                'verbose_name': 'Server order',
                'verbose_name_plural': 'Server orders',
            },
            bases=('order.baseorder',),
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('baseorder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='order.BaseOrder')),
                ('client', models.ForeignKey(to='client.Client')),
                ('shop', models.ForeignKey(to='shop.Shop')),
            ],
            options={
                'verbose_name': 'Shop order',
                'verbose_name_plural': 'Shop orders',
            },
            bases=('order.baseorder',),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
