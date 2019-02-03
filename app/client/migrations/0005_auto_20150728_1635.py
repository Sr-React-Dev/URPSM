# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_auto_20150728_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='ref',
            field=models.CharField(default=210793999, unique=True, max_length=50),
        ),
    ]
