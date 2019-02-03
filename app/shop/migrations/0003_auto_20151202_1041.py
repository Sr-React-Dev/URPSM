# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_shop_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='city',

        ),
        migrations.AddField(
            model_name='shop',
            name='city',
            field=models.ForeignKey(to='simplecities.City', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(
                chained_model_field=b'country', default=0, auto_choose=True, to='simplecities.City', chained_field=b'country'),
            preserve_default=False,
        ),
    ]
