# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0022_merge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='endpoint',
            unique_together=set([('url',)]),
        ),
    ]
