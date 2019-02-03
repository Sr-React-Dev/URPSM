# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='unconfirmed_email',
            field=models.EmailField(max_length=75, verbose_name='Unconfirmed email', blank=True),
            preserve_default=True,
        ),
    ]
