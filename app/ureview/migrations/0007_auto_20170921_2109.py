# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0018_charges'),
        ('server', '0017_auto_20170921_2109'),
        ('ureview', '0006_auto_20161125_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=1024, verbose_name='Content', blank=True)),
                ('language', models.CharField(max_length=10, verbose_name='Language', blank=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date')),
                ('rating', models.FloatField(default=0, verbose_name='rating')),
                ('order', models.ForeignKey(blank=True, to='order.ServerOrder', null=True)),
                ('server', models.ForeignKey(blank=True, to='server.Server', null=True)),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'reviewed order',
                'verbose_name_plural': 'reviewed orders',
            },
        ),
        migrations.RemoveField(
            model_name='reviewedorder',
            name='client',
        ),
        migrations.RemoveField(
            model_name='reviewedorder',
            name='server',
        ),
        migrations.RemoveField(
            model_name='reviewedorder',
            name='server_order',
        ),
        migrations.RemoveField(
            model_name='reviewedorder',
            name='shop',
        ),
        migrations.RemoveField(
            model_name='reviewedorder',
            name='shop_order',
        ),
        migrations.DeleteModel(
            name='ReviewedOrder',
        ),
    ]
