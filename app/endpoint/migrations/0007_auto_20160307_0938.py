# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0006_endpoint_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='service',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
