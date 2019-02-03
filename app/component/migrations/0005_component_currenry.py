# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0004_component_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='currenry',
            field=models.CharField(default=b'USD', max_length=64, choices=[(b'EUR', '\u20ac'), (b'USD', '$')]),
        ),
    ]
