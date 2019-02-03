# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20160927_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='server',
            name='server_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='server_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'eg: +212612345678', max_length=128, null=True, blank=True),
        ),
    ]
