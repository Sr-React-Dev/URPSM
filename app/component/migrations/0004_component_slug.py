# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='slug',
            field=models.SlugField(default='', editable=False),
            preserve_default=False,
        ),
    ]
