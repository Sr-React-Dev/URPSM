# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0018_auto_20170108_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='networks',
            field=models.ManyToManyField(default=None, to='endpoint.Network', null=True, blank=True),
        ),
        # migrations.AlterField(
        #     model_name='endpoint',
        #     name='url',
        #     field=models.URLField(unique=True),
        # ),
        migrations.AlterUniqueTogether(
            name='endpoint',
            unique_together=set([('url',)]),
        ),
        # migrations.RemoveField(
        #     model_name='endpoint',
        #     name='network',
        # ),
    ]
