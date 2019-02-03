# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20151202_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='country',

        ),
        migrations.AddField(
            model_name='shop',
            name='country',
            field=models.ForeignKey(to='simplecities.Country', blank=True, null=True),
        ),
        # migrations.AlterField(
        #     model_name='shop',
        #     name='country',
        #     field=models.ForeignKey(to='simplecities.Country'),
        # ),
    ]
