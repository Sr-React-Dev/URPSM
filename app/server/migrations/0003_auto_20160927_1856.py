# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20160924_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='paypal_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='server_email',
            field=models.EmailField(max_length=254),
        ),
    ]
