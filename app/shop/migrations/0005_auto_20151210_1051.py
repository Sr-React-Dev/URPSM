# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20151203_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='country',
            field=models.ForeignKey(to='simplecities.Country'),
        ),
    ]
