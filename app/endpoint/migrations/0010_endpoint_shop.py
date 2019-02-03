# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_banner_active'),
        ('endpoint', '0009_auto_20160310_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='shop',
            field=models.ForeignKey(default=1, to='shop.Shop'),
            preserve_default=False,
        ),
    ]
