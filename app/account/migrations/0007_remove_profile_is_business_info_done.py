# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20161028_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_business_info_done',
        ),
    ]
