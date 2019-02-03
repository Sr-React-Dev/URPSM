# Created by Vishwash Gupta

from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
from app.order.models import ServerOrder

ORDER_TICKET_REASONS = (
    ("WRONG_CODE", "WRONG_CODE"),
    ("ITEM_DEFECTIVE", "ITEM_DEFECTIVE"),
)

COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"
ADMIN_SUPPORT = "ADMIN_SUPPORT"
INITIATED = "INITIATED"

TICKET_RESPONSES = (
    (COMPLETED, COMPLETED),
    (CANCELLED, CANCELLED),
    (ADMIN_SUPPORT, ADMIN_SUPPORT),
)

TICKET_STATUSES = (
    (INITIATED, INITIATED),
    (ADMIN_SUPPORT, ADMIN_SUPPORT),
    (COMPLETED, COMPLETED),
)


def get_ticket_file_upload_to(self, instance):
    print "filename : ", self
    print "file ext : ", instance
    return "static/ticket_files/%s" % str(uuid.uuid4().hex[:6].upper()) + "_" + instance


class FileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    uploaded_file = models.FileField(upload_to=get_ticket_file_upload_to, null=False, blank=False)
    actual_file_name = models.CharField(null=False, max_length=255, blank=False)
    file_extension_name = models.CharField(null=False, max_length=255, blank=False)


class OrderTicket(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(null=True)
    last_updated_at = models.DateTimeField(null=True)
    server_order = models.ForeignKey(ServerOrder, related_name="order_tickets")
    shop_reason = models.TextField(null=True, blank=True)
    server_reason = models.TextField(null=True, blank=True)
    admin_reason = models.TextField(null=True, blank=True)
    shop_admin_support_reason = models.TextField(null=True, blank=True)
    server_admin_support_reason = models.TextField(null=True, blank=True)
    shop_comments = models.TextField(null=True, blank=True)
    shop_comments_time = models.DateTimeField(null=True)
    server_comments = models.TextField(null=True, blank=True)
    server_comments_time = models.DateTimeField(null=True)
    server_response = models.CharField(max_length=255, choices=TICKET_RESPONSES, null=True)
    server_response_time = models.DateTimeField(null=True)
    shop_response = models.CharField(max_length=255, choices=TICKET_RESPONSES, null=True)
    shop_response_time = models.DateTimeField(null=True)
    admin_response = models.CharField(max_length=255, choices=TICKET_RESPONSES, null=True)
    admin_response_time = models.DateTimeField(null=True)
    admin_support_required = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=TICKET_STATUSES)
    server_files = models.ManyToManyField(FileUpload, related_name='server_files')
    shop_files = models.ManyToManyField(FileUpload, related_name='shop_files')

    def save(self, *args, **kwargs):
        self.last_updated_at = timezone.now()
        super(OrderTicket, self).save(*args, **kwargs)


class TicketMessage(models.Model):
    id = models.AutoField(primary_key=True)
    order_ticket = models.ForeignKey(OrderTicket)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', null=False, blank=False)
    message_text = models.TextField(null=True, blank=True)
    message_files = models.ManyToManyField(FileUpload, related_name='message_files')