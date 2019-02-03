# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_auto_20150728_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='ref',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
