# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0007_auto_20170830_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyvaluestore',
            name='key',
            field=models.TextField(),
        ),
    ]
