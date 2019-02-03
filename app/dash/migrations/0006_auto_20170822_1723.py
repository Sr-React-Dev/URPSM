# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [('dash', '0005_auto_20170730_0548')]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=60)),
                ('type', models.CharField(max_length=30, choices=[(b'ADMINISTRATIVE', b'ADMINISTRATIVE'), (b'TECHNICAL', b'TECHNICAL'), (b'FINANCIAL', b'FINANCIAL')])),
                ('active', models.BooleanField(default=True)),
                ('status', models.CharField(default=b'OPEN', max_length=30, choices=[(b'OPEN', b'OPEN'), (b'SOLVED', b'SOLVED')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('server', models.ForeignKey(default=None, to='server.Server', null=True)),
                ('shop', models.ForeignKey(default=None, to='shop.Shop', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='dash.MessageThread'),
        ),
    ]
