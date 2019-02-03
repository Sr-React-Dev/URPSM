# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20170418_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=9, decimal_places=2)),
                ('method', models.CharField(max_length=30, choices=[(b'WESTERNUNION', b'WESTERNUNION'), (b'MONEYGRAM', b'MONEYGRAM'), (b'WAFACASH', b'WAFACASH')])),
                ('status', models.CharField(default=b'UNPAID', max_length=10, choices=[(b'PAID', b'PAID'), (b'UNPAID', b'UNPAID')])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SFileUpload',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uploaded_file', models.FileField(upload_to=app.shop.models.get_invoice_file_upload_to)),
                ('actual_file_name', models.CharField(max_length=255)),
                ('file_extension_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='invoices',
            name='files_admin',
            field=models.ManyToManyField(related_name='proof_admin_files', to='shop.SFileUpload'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='files_shop',
            field=models.ManyToManyField(related_name='proof_shop_files', to='shop.SFileUpload'),
        ),
    ]
