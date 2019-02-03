# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0008_auto_20160307_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='service',
            field=models.TextField(),
        ),
    ]
