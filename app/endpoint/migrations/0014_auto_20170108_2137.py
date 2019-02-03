# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0013_auto_20160924_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('services', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='endpoint',
            name='provider',
            field=models.CharField(default=b'dhru', max_length=16, choices=[(b'', b''), (b'dhru', b'DHRU'), (b'naksh', b'Naksh Soft')]),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='server',
            field=models.ForeignKey(related_name='server_endpoint', to='server.Server', null=True),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='url',
            field=models.URLField(unique=True),
        ),
        # migrations.AlterUniqueTogether(
        #     name='endpoint',
        #     unique_together=set([('url',)]),
        # ),
        # migrations.RemoveField(
        #     model_name='endpoint',
        #     name='network',
        # ),
        migrations.RemoveField(
            model_name='endpoint',
            name='service',
        ),
        migrations.AddField(
            model_name='endpoint',
            name='networks',
            field=models.ManyToManyField(default=None, to='endpoint.Network', blank=True),
        ),
    ]
