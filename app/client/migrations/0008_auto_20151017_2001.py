# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0006_auto_20151003_1107'),
        ('client', '0007_auto_20150728_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='addon',
            name='type',
            field=models.ForeignKey(related_name='addons_type', default='', to='component.Type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addon',
            name='client',
            field=models.ForeignKey(related_name='addons_client', to='client.Client'),
        ),
        migrations.AlterUniqueTogether(
            name='addon',
            unique_together=set([('type', 'client')]),
        ),
        migrations.RemoveField(
            model_name='addon',
            name='name',
        ),
    ]
