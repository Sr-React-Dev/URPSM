# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0004_adminactionhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminactionhistory',
            name='affected',
            field=models.TextField(null=True, blank=True),
        ),
    ]
