# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20150728_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='ref',
            field=models.CharField(default=789698031, unique=True, max_length=50),
        ),
    ]
