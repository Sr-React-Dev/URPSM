# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0002_auto_20161205_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyValueStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=60)),
                ('category', models.CharField(max_length=30, null=True, blank=True)),
                ('value', models.TextField(max_length=2048, blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
