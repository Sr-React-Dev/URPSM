# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'John Doe', max_length=50)),
                ('subject', models.CharField(default=b'Hello', max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(default=b'', null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(max_length=2048)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
