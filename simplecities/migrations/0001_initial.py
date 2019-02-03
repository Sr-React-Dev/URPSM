# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('alternatives', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('code_fips', models.CharField(max_length=5)),
                ('code_iso', models.CharField(max_length=5)),
                ('tld', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'country', chained_field=b'country', auto_choose=True, to='simplecities.City')),
                ('country', models.ForeignKey(to='simplecities.Country')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='country',
            unique_together=set([('name', 'code_iso'), ('name', 'code_fips')]),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='simplecities.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('country', 'name')]),
        ),
    ]
