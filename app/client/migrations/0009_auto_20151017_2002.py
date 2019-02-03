# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_auto_20151017_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='type',
            field=models.ForeignKey(related_name='addons_type', blank=True, to='component.Type', null=True),
        ),
    ]
