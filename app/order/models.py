# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json
from django.db import models
# from uuidfield import UUIDField
from app.shop.models import Shop
from app.server.models import Server
from app.client.models import Client
from app.endpoint.models import Endpoint
from app.phone.models import Brand, Model
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator
from app.antifraud.validators import validate_imei

PENDING     = 'PENDING'
DELIVERED   = 'DELIVERED'
REJECTED    = 'REJECTED'
CANCELLED   = 'CANCELLED'
COMPLETED   = 'COMPLETED'
HOLD        = 'HOLD'
CANT_REPAIR = 'CANT_REPAIR'
NEED_YOUR_CALL = 'NEED_YOUR_CALL'
READY          = 'READY'

ORDER_STATUSES = (
    (PENDING, 'PENDING'),
    (DELIVERED, 'DELIVERED'),
    (REJECTED, 'REJECTED'),
    (CANCELLED, 'CANCELLED'),
    (COMPLETED, 'COMPLETED'),
    (HOLD, 'HOLD')
)
SHOP_ORDER_STATUSES = (
        (PENDING,'PENDING'),
        (READY,'READY'),
        (NEED_YOUR_CALL,'NEED_YOUR_CALL'),
        (CANT_REPAIR,'CANT_REPAIR'),
    )

class BaseOrder(models.Model):
    ref           = models.CharField(max_length=255)
    imei          = models.CharField(max_length=15, validators=[validate_imei])
    brand         = models.ForeignKey(Brand, related_name="order_brand", blank=True, null=True, default=None)
    model         = models.ForeignKey(Model, related_name="order_model", blank=True, null=True, default=None)
    amount        = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=0)
    paid          = models.BooleanField(default=False, editable=True)
    created       = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    deleted       = models.BooleanField(default=False, editable=True)


    def __str__(self):
        return self.ref
        
    # class Meta:
    #     abstract = True

class Charges(models.Model):
    charge = models.CharField(max_length=30,unique=True)
    value = models.CharField(max_length=4)

class ServerOrder(BaseOrder):
    shop = models.ForeignKey(Shop, related_name="shop_server_order")
    server = models.ForeignKey(Server, related_name="server_order")
    endpoint = models.ForeignKey(Endpoint)
    service = models.CharField(max_length=255)
    cancellation_time = models.DateTimeField(blank=True, null=True)
    urpsm_charge = models.DecimalField(max_digits=12, decimal_places=2, default='0', null=False, blank=False)
    urpsm_charge_factor = models.DecimalField(max_digits=12, decimal_places=2, default='0', null=False, blank=False)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default='0', null=False, blank=False)
    status = models.CharField(choices=ORDER_STATUSES, null=False, default=COMPLETED, max_length=255)

    @property
    def get_service(self):
        return unicode(self.service)

    class Meta:
        verbose_name        = "Server order"
        verbose_name_plural = "Server orders"


class ShopOrder(BaseOrder):
    shop = models.ForeignKey(Shop, related_name="client_server_order")
    client = models.ForeignKey(Client)
    status = models.CharField(choices=SHOP_ORDER_STATUSES, null=False, default=READY, max_length=255)

    class Meta:
        verbose_name        = "Shop order"
        verbose_name_plural = "Shop orders"


# class Order(models.Model):
# # uuid = UUIDField(auto=True)
# ref = models.CharField(max_length=255)
#     imei = models.CharField(max_length=15)
#     shop = models.ForeignKey(Shop)
#     endpoint = models.ForeignKey(Endpoint)
#     service = models.CharField(max_length=255)
#     amount  = models.CharField(max_length=50, default='0')
#     paid    = models.BooleanField(default=False, editable=True)

#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"

#     def __str__(self):
#         return self.imei

#     @property
#     def get_service(self):
#         services = json.loads(self.endpoint.service)
#         return unicode(services.get(self.service))