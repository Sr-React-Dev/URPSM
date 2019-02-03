# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0015_endpoint_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('services', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
           model_name='endpoint',
           name='network'
        ),
        migrations.RemoveField(
           model_name='endpoint',
           name='service'
        ),
        migrations.AddField(
            model_name='endpoint',
            name='networks',
            field=models.ForeignKey(default=None, blank=True, to='endpoint.Network', null=True),
        ),
    ]
