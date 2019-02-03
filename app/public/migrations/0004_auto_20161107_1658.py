# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0003_contact_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='feedback',
            field=models.TextField(default=b'', max_length=2048, null=True, blank=True),
        ),
    ]
