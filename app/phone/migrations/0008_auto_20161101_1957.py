# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0007_auto_20151119_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('repairing_request', models.PositiveIntegerField(default=0)),
                ('repaired_items', models.PositiveIntegerField(default=0)),
                ('unlocking_request', models.PositiveIntegerField(default=0)),
                ('unlocked_items', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='model',
            name='stats',
            field=models.ForeignKey(related_name='model_stats', default=b'', blank=True, to='phone.Stat', null=True),
        ),
    ]
