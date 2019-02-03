# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20160924_1836'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('server', '0004_auto_20161004_1546'),
        ('shop', '0010_auto_20161004_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(max_length=1, choices=[(b'L', 'New review from client'), (b'D', 'Order cancelling refused'), (b'B', 'Order done'), (b'M', 'Abuse report confirmed'), (b'C', 'New review from shop'), (b'F', 'New review from server'), (b'A', 'New ticket'), (b'W', 'One order canceled'), (b'E', 'New component'), (b'S', 'Validate order cancelling'), (b'K', 'Abuse report declined'), (b'J', 'New client request'), (b'T', 'New order')])),
                ('is_read', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('server', models.ForeignKey(related_name='server', blank=True, to='server.Server', null=True)),
                ('server_order', models.ForeignKey(related_name='server_order', blank=True, to='order.ServerOrder', null=True)),
                ('shop', models.ForeignKey(related_name='shop', blank=True, to='shop.Shop', null=True)),
                ('shop_order', models.ForeignKey(related_name='shop_order', blank=True, to='order.ShopOrder', null=True)),
                ('to_user', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
