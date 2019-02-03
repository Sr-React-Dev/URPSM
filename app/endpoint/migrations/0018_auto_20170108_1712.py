# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0017_auto_20170108_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='services',
            field=models.TextField(),
        ),
    ]
