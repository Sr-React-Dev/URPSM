# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20161004_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='server',
            name='server_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='server',
            name='server_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'eg: +212612345678', max_length=128),
        ),
    ]
