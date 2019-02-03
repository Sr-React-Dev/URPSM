# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default=b'Hello', max_length=255)),
                ('type', models.CharField(default=b'', max_length=5, null=True, blank=True, choices=[(b'', b''), (b'admin', 'administrative'), (b'tech', 'technical'), (b'money', 'Finantial')])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(max_length=2048)),
                ('feedback', models.TextField(default=b'', max_length=2048, null=True, blank=True)),
                ('processed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
