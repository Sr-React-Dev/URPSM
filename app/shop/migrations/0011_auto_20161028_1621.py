# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20161004_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='shop',
            name='shop_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'eg: +212612345678', max_length=128),
        ),
    ]
