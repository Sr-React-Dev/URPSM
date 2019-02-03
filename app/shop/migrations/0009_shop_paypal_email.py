# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_banner_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='paypal_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
