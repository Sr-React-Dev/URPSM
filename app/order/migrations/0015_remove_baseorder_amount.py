# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20161205_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseorder',
            name='amount',
        ),
    ]
