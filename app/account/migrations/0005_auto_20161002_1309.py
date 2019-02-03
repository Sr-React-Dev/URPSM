# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.account.managers


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20160924_2220'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', app.account.managers.ProfileManager()),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='unconfirmed_email',
            field=models.EmailField(max_length=254, verbose_name='Unconfirmed email', blank=True),
        ),
    ]
