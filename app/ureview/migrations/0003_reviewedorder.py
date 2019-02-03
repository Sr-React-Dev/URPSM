# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20161030_1735'),
        ('shop', '0012_shop_average_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('server', '0006_server_average_rating'),
        ('ureview', '0002_auto_20161029_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewedOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, choices=[(b'U', 'Ticketed and solved for server owner'), (b'S', 'Ticketed and solved for shop owner'), (b'C', 'Ticketed and solved for phone owner'), (b'D', 'Successfully Delivered '), (b'D', 'Successfully Repaired ')])),
                ('client', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('server', models.ForeignKey(blank=True, to='server.Server', null=True)),
                ('server_order', models.ForeignKey(blank=True, to='order.ServerOrder', null=True)),
                ('shop', models.ForeignKey(blank=True, to='shop.Shop', null=True)),
                ('shop_order', models.ForeignKey(blank=True, to='order.ShopOrder', null=True)),
            ],
            options={
                'verbose_name': 'reviewed order',
                'verbose_name_plural': 'reviewed orders',
            },
        ),
    ]
