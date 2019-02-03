# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.ticket.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uploaded_file', models.FileField(upload_to=app.ticket.models.get_ticket_file_upload_to)),
                ('actual_file_name', models.CharField(max_length=255)),
                ('file_extension_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TicketMessage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message_text', models.TextField(null=True, blank=True)),
                ('message_files', models.ManyToManyField(related_name='message_files', to='ticket.FileUpload')),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='orderticket',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='orderticket',
            name='reason',
        ),
        migrations.AddField(
            model_name='orderticket',
            name='admin_reason',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='admin_response',
            field=models.CharField(max_length=255, null=True, choices=[(b'COMPLETED', b'COMPLETED'), (b'CANCELLED', b'CANCELLED'), (b'ADMIN_SUPPORT', b'ADMIN_SUPPORT')]),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='admin_response_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='last_updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='server_admin_support_reason',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='server_comments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='server_comments_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='server_reason',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='shop_admin_support_reason',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='shop_comments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='shop_comments_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='shop_reason',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='orderticket',
            name='server_order',
            field=models.ForeignKey(related_name='order_tickets', to='order.ServerOrder'),
        ),
        migrations.AlterField(
            model_name='orderticket',
            name='server_response',
            field=models.CharField(max_length=255, null=True, choices=[(b'COMPLETED', b'COMPLETED'), (b'CANCELLED', b'CANCELLED'), (b'ADMIN_SUPPORT', b'ADMIN_SUPPORT')]),
        ),
        migrations.AlterField(
            model_name='orderticket',
            name='shop_response',
            field=models.CharField(max_length=255, null=True, choices=[(b'COMPLETED', b'COMPLETED'), (b'CANCELLED', b'CANCELLED'), (b'ADMIN_SUPPORT', b'ADMIN_SUPPORT')]),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.AddField(
            model_name='ticketmessage',
            name='order_ticket',
            field=models.ForeignKey(to='ticket.OrderTicket'),
        ),
        migrations.AddField(
            model_name='ticketmessage',
            name='sender',
            field=models.ForeignKey(related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='server_files',
            field=models.ManyToManyField(related_name='server_files', to='ticket.FileUpload'),
        ),
        migrations.AddField(
            model_name='orderticket',
            name='shop_files',
            field=models.ManyToManyField(related_name='shop_files', to='ticket.FileUpload'),
        ),
    ]
