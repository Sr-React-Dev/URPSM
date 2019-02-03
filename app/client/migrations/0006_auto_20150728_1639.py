# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20150728_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='ref',
            field=models.CharField(default=697927624, unique=True, max_length=50),
        ),
    ]
