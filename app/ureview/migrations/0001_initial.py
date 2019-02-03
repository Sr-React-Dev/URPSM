# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20161028_1621'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('server', '0005_auto_20161028_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=1024, verbose_name='Content', blank=True)),
                ('language', models.CharField(max_length=10, verbose_name='Language', blank=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date')),
                ('average_rating', models.FloatField(default=0, verbose_name='Average rating')),
                ('server', models.ForeignKey(default=False, to='server.Server')),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-creation_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=1024, verbose_name='Content', blank=True)),
                ('language', models.CharField(max_length=10, verbose_name='Language', blank=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date')),
                ('average_rating', models.FloatField(default=0, verbose_name='Average rating')),
                ('shop', models.ForeignKey(default=False, to='shop.Shop')),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-creation_date'],
                'abstract': False,
            },
        ),
    ]
