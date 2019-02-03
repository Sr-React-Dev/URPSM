# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_profile_is_business_info_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ip_address',
            field=models.CharField(max_length=40, null=True, verbose_name='current ip', blank=True),
        ),
    ]
