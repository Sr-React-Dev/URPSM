# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_auto_20161213_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='balance',
            new_name='credit',
        ),
    ]
