# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_contact_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
