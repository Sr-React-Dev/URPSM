# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0017_auto_20170921_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='max_allowed_apis',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
