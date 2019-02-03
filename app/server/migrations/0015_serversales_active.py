# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0014_serversales'),
    ]

    operations = [
        migrations.AddField(
            model_name='serversales',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
