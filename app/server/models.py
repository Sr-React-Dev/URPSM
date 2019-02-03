# -*- coding: utf-8 -*-
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
import ast, itertools

from uuidfield import UUIDField
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField
# from easy_thumbnails.fields import ThumbnailerImageField
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage
# from mobilify.custom_storages import StaticStorage
from slugify import slugify

from smart_selects.db_fields import ChainedForeignKey
from simplecities.models import City, Country
# from app.endpoint.models import Endpoint

from app.search.index import Indexed, SearchField, FilterField, RelatedFields


LEVEL_1 = "1"
LEVEL_2 = "2"
LEVEL_3 = "3"
LEVEL_4 = "4"
LEVEL_5 = "5"

LEVELS = (('Level 1 ', LEVEL_1),('Level 2 ', LEVEL_2),('Level 3 ', LEVEL_3),('Level 4 ', LEVEL_4),('Level 5 ', LEVEL_5))




class Server(models.Model):

    """
    Description: Server Model
    """

    uuid = UUIDField(auto=True)
    name = models.CharField(
        max_length=255, unique=True)
    slug = models.SlugField(editable=False, db_index=True)
    credit = models.DecimalField(
        max_digits=9, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))], default=0, blank=True)
    # balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    logo = VersatileImageField(
        upload_to='server/%Y/%m/', blank=True, null=True,
         placeholder_image=OnStoragePlaceholderImage(
            path='icons/default_server.png',
            # storage=StaticStorage()
            ),
        default='icons/default_server.png'
        )
    description = models.TextField(null=True, blank=True)

    vat = models.PositiveIntegerField(default=0, help_text="VAT eg: 20")

    server_phone = PhoneNumberField(help_text='eg: +212612345678')
    server_email = models.EmailField()
    country = models.ForeignKey(Country)
    city = ChainedForeignKey(
        City,
        chained_field="country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True
    )
    address = models.CharField(max_length=300)
    location = PlainLocationField(
        based_fields=[country, city, address], zoom=13, blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)

    paypal_email = models.EmailField(blank=True, null=True)

    blocked   = models.BooleanField(default=False)
    

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    average_rating = models.FloatField(blank=True, null=True)

    level   = models.CharField(max_length=1, null=False, choices=LEVELS, default=LEVEL_1)
    rank    = models.PositiveIntegerField(default=0)
    performance    = models.PositiveIntegerField(default=0)
    completion_charges = models.CharField(max_length=4, null=True, default=None, blank=True)

    max_allowed_apis = models.PositiveIntegerField(default=1)


    def get_unlocked_phones_count(self):
        # try:
        return self.server_order.filter(status='COMPLETED').count() or 0
        # except:
            # return 0

    def get_services_count(self):
        try:
            networks = [ e.networks.all() for e in self.server_endpoint.all() ]
            networks = itertools.chain.from_iterable(networks)
            c = sum([len(ast.literal_eval(n.services)) for n in networks])
            return c
        except Exception as e:
            print e
            return 0
    def get_network_count(self):
        try:
            i = 0
            c = [ i + e.networks.count() for e in self.server_endpoint.all()  ][0]
            return c
        except Exception as e:
            print e
            return 0

    def __str__(self):
        return unicode(self.name)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.average_rating = self.calculate_rating()['avg_rating']
        super(Server, self).save(*args, **kwargs)

    def calculate_rating(self):
        return self.review_server.aggregate(avg_rating = models.Avg('rating'))


sales_dash_choice =(('upcoming_payments','upcoming_payments'),
                    ('available_withdraw','available_withdraw'),
                    ('already_withdrawn','already_withdrawn'),
                    ('amount_completed','amount_completed'))


class ServerSales(models.Model):
    server = models.ForeignKey(Server)
    type = models.CharField(choices=sales_dash_choice,max_length=30)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    active = models.NullBooleanField(default=False,null=True)
    desc = models.CharField(max_length=50,null=True,blank=True)