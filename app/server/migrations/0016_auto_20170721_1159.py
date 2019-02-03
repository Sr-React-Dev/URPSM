# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0015_serversales_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='serversales',
            name='desc',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='serversales',
            name='active',
            field=models.NullBooleanField(default=False),
        ),
    ]
