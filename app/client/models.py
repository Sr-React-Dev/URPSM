from __future__ import absolute_import
#from random import randint
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.aggregates import Sum

from uuidfield import UUIDField
from phonenumber_field.modelfields import PhoneNumberField
from easy_thumbnails.fields import ThumbnailerImageField
from smart_selects.db_fields import ChainedForeignKey

from app.shop.models import Shop
from app.phone.models import Brand, Model
from app.component.models import Type
from app.antifraud.validators import validate_imei



class Client(models.Model):

    """
    Description: Client phone mobile
    """
    STATUS_CHOICES = (
        ('p', "Pending"),
        ('c', "Need Your Call"),
        ('r', "Ready"),
        ('n', "Can't Repaired"),
    )

    TODO_CHOICES = (
        ('r', "Repairing"),
        ('f', "Flashing"),
        ('u', "Unlocking"),
    )

    uuid = UUIDField(auto=True)
    # Adding model and brand
    brand = models.ForeignKey(Brand, related_name='client_brand')
    model = ChainedForeignKey(Model,
                              chained_field='brand',
                              chained_model_field='brand',
                              show_all=False, 
                              auto_choose=True,
                              related_name="client_model"
                              )
    ref = models.CharField(max_length=50, unique=True)
    shop = models.ForeignKey(Shop, related_name='phone_shop')
    serial = models.CharField(max_length=255, blank=True, null=True)
    imei = models.CharField(max_length=255, validators=[validate_imei])
    phone_number = PhoneNumberField(help_text='eg: +212612345678')
    email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    status = models.CharField(
        max_length=64, choices=STATUS_CHOICES, default='p')
    status_description = models.TextField(blank=True, null=True)

    todo = models.CharField(max_length=64, choices=TODO_CHOICES, default='r')
    todo_description = models.TextField(blank=True, null=True)

    paid = models.BooleanField(default=False)
    paid_for = models.ForeignKey(User, null=True, blank=True)

    delivery_time = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-created']

    def __str__(self):
        return unicode(self.shop)

    @property
    def subtotal(self):
        addons_amount = self.addons_phone.aggregate(
            addons=Sum('price'))['addons'] or 0
        return self.amount + addons_amount

    @property
    def vat(self):
        return (self.subtotal * self.shop.vat) / 100

    @property
    def total(self):
        return self.subtotal + self.vat

    @property
    def total_benefit(self):
        addons_amount = self.addons_phone.aggregate(
            addons=Sum('price'))['addons'] or 0
        addons_original_amount = self.addons_phone.aggregate(
            addons=Sum('original_price'))['addons'] or 0
        return self.amount + (addons_amount - addons_original_amount)

    @property 
    def satisfied_clients_count(self):
        pass

    # @property 
    # def repaired_phones_by_model(self, model):
    #     model = Model.objects.get(pk=model)
    #     return self.
    
    



class Addon(models.Model):
    type = models.ForeignKey(
        Type, related_name='addons_type', null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=0, help_text='Addon selling price.')
    original_price = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=0, help_text='Addon original price.')
    client = models.ForeignKey(Client, related_name='addons_phone')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return unicode(self.client)

    class Meta:
        unique_together = (('type', 'client'),)

    @property
    def benefit(self):
        return self.price - self.original_price
        
from versatileimagefield.fields import VersatileImageField

class Image(models.Model):
    image = VersatileImageField(upload_to='phone/%Y/%m/')
    client = models.ForeignKey(Client, related_name='images_phone')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return unicode(self.client)
