# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0005_component_currenry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='component',
            old_name='currenry',
            new_name='currency',
        ),
    ]
