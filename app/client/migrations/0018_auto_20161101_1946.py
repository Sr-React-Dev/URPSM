# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_auto_20161002_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='brand',
            field=models.ForeignKey(related_name='client_brand', to='phone.Brand'),
        ),
        migrations.AlterField(
            model_name='client',
            name='model',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, related_name='client_model', chained_model_field=b'brand', to='phone.Model', chained_field=b'brand'),
        ),
    ]
