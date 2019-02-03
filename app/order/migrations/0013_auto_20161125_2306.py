# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_baseorder_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoporder',
            name='client',
            field=models.ForeignKey(to='client.Client'),
        ),
    ]
