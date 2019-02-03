# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20150728_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='deleted',
        ),
        migrations.AlterField(
            model_name='client',
            name='ref',
            field=models.CharField(default=106025757, unique=True, max_length=50),
        ),
    ]
