# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20151210_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner', models.ImageField(upload_to=b'banners/')),
                ('link', models.URLField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
