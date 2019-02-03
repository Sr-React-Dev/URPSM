# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ureview', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serverreview',
            name='average_rating',
        ),
        migrations.RemoveField(
            model_name='shopreview',
            name='average_rating',
        ),
        migrations.AddField(
            model_name='serverreview',
            name='rating',
            field=models.FloatField(default=0, verbose_name='rating'),
        ),
        migrations.AddField(
            model_name='shopreview',
            name='rating',
            field=models.FloatField(default=0, verbose_name='rating'),
        ),
    ]
