# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0009_auto_20161019_0050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('message_text', models.CharField(max_length=255)),
                ('receiver', models.ForeignKey(related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderTicket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('reason', models.CharField(max_length=255, choices=[(b'WRONG_CODE', b'WRONG_CODE'), (b'ITEM_DEFECTIVE', b'ITEM_DEFECTIVE')])),
                ('comments', models.CharField(max_length=255, null=True)),
                ('server_response', models.CharField(max_length=255, null=True, choices=[(b'ACCEPTED', b'ACCEPTED'), (b'CANCELLED', b'CANCELLED'), (b'ADMIN_SUPPORT', b'ADMIN_SUPPORT')])),
                ('server_response_time', models.DateTimeField(null=True)),
                ('shop_response', models.CharField(max_length=255, null=True, choices=[(b'ACCEPTED', b'ACCEPTED'), (b'CANCELLED', b'CANCELLED'), (b'ADMIN_SUPPORT', b'ADMIN_SUPPORT')])),
                ('shop_response_time', models.DateTimeField(null=True)),
                ('admin_support_required', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=255, choices=[(b'INITIATED', b'INITIATED'), (b'ADMIN_SUPPORT', b'ADMIN_SUPPORT'), (b'COMPLETED', b'COMPLETED')])),
                ('server_order', models.ForeignKey(to='order.ServerOrder')),
            ],
        ),
    ]
