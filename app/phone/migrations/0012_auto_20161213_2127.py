# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0011_model_satisfied_clients_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='picture',
            field=models.ImageField(default=b'icons/default_phone.png', null=True, upload_to=b'phone/', blank=True),
        ),
    ]
