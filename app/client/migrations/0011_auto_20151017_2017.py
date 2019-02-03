# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_addon_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='client',
            field=models.ForeignKey(related_name='addons_phone', to='client.Client'),
        ),
    ]
