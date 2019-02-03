# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20161019_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoporder',
            name='status',
            field=models.CharField(default=b'READY', max_length=255, choices=[(b'PENDING', b'PENDING'), (b'READY', b'READY'), (b'NEED_YOUR_CALL', b'NEED_YOUR_CALL'), (b'CANT_REPAIR', b'CANT_REPAIR')]),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='client',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
