# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0007_auto_20151210_1051'),
        ('phone', '0011_model_satisfied_clients_count'),
        ('notifications', '0005_notification_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='brand',
            field=models.ForeignKey(related_name='notif_brand', blank=True, to='phone.Brand', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='component',
            field=models.ForeignKey(related_name='notif_component', blank=True, to='component.Component', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='model',
            field=models.ForeignKey(related_name='notif_model', blank=True, to='phone.Model', null=True),
        ),
    ]
