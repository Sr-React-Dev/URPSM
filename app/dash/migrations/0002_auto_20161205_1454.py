# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactadmin',
            options={'verbose_name': 'Admin Contact', 'verbose_name_plural': 'Admin Contacts'},
        ),
        migrations.AlterField(
            model_name='contactadmin',
            name='type',
            field=models.CharField(default=b'', max_length=5, null=True, blank=True, choices=[(b'', b'--'), (b'admin', 'administrative'), (b'tech', 'technical'), (b'money', 'financial')]),
        ),
    ]
