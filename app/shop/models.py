# -*- coding: utf-8 -*-
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


from uuidfield import UUIDField
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage

from django.conf import settings

from mobilify.custom_storages import StaticStorage
from slugify import slugify
from app.search.index import Indexed, SearchField, FilterField, RelatedFields
from smart_selects.db_fields import ChainedForeignKey
from simplecities.models import City, Country
import uuid


LEVEL_1 = "1"
LEVEL_2 = "2"
LEVEL_3 = "3"
LEVEL_4 = "4"
LEVEL_5 = "5"

LEVELS = (('Level 1 ', LEVEL_1),('Level 2 ', LEVEL_2),('Level 3 ', LEVEL_3),('Level 4 ', LEVEL_4),('Level 5 ', LEVEL_5))

class ShopQueryset(models.QuerySet):
    def locations(self):
        result_list = []

        locations =  self.values('location')
        for location in locations:
            shop_latitude, shop_longitude = location.split(',')
            if shop_latitude <= max_east and shop_latitude >=max_west:
                if shop_longitude <= max_south and shop_longitude >=max_north:
                    result_list.append(shop)
        return result_list

payment_choices = (('WESTERNUNION','WESTERNUNION'),('MONEYGRAM','MONEYGRAM'),('WAFACASH','WAFACASH'),('BANK','BANK'),('BITCOIN','BITCOIN'))

def get_invoice_file_upload_to(self, instance):
    print "filename : ", self
    print "file ext : ", instance
    return "static/invoice_files/%s" % str(uuid.uuid4().hex[:6].upper()) + "_" + instance

class SFileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    uploaded_file = models.FileField(upload_to=get_invoice_file_upload_to, null=False, blank=False)
    actual_file_name = models.CharField(null=False, max_length=255, blank=False)
    file_extension_name = models.CharField(null=False, max_length=255, blank=False)



class ShopManager(models.Manager):
    def get_queryset(self):
        return ShopQueryset(self.model, using=self._db)

    def get_shops_by_coords(self, latLng, ray=0.5):
        
        
        return result_list

def a_get_satisfied_clients_count(shop):
    from app.ureview.models import ShopReview
    return ShopReview.objects.filter(shop=shop,rating__gte=4).distinct().count() or 0



class Shop(models.Model, Indexed):

    """
    Description: Shop Model
    """

    uuid = UUIDField(auto=True)
    name = models.CharField(
        max_length=255, unique=True)
    slug = models.SlugField(editable=False, db_index=True)
    balance = models.DecimalField(
        max_digits=9, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))], default=0, blank=True)
    # balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    logo = VersatileImageField(
        upload_to='shop/%Y/%m/', blank=True, null=True, placeholder_image=OnStoragePlaceholderImage(
            path='icons/default_store.png',),
        default='icons/default_store.png')
    description = models.TextField(null=True, blank=True)

    vat = models.PositiveIntegerField(default=0, help_text="VAT eg: 20")

    shop_phone = PhoneNumberField(help_text='eg: +212612345678')
    shop_email = models.EmailField()
    # country = CountryField()
    # city = models.CharField(max_length=255, blank=True, null=True)
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

    level   = models.CharField(max_length=1, blank=True, null=True, choices=LEVELS, default=LEVEL_1)
    rank    = models.PositiveIntegerField(blank=True, null=True, default=0)
    performance = models.PositiveIntegerField(blank=True, null=True, default=0)
    cancellation_charges = models.CharField(max_length=4,null=True,default=None,blank=True)
    completion_charges = models.CharField(max_length=4,null=True,default=None,blank=True)

    search_fields = [
        SearchField('name', partial_match=True, boost=10),
        SearchField('slug'),
        SearchField('description', partial_match=True, boost=5),
        SearchField('address', partial_match=True, boost=5),
        SearchField('location'),
        SearchField('website'),
        FilterField('average_rating'),
        FilterField('blocked'),
        SearchField('facebook'),
        SearchField('twitter'),
        SearchField('google_plus'),
        FilterField('level'),
        FilterField('rank'),
        FilterField('performance'),
        RelatedFields('city', [
            SearchField('name')
        ]),
        RelatedFields('country', [
            SearchField('name'),
            SearchField('code_fips'),
            SearchField('code_iso'),
        ])
        ]

    def __str__(self):
        return unicode(self.name)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.average_rating = self.calculate_rating()['avg_rating']
        super(Shop, self).save(*args, **kwargs)

    def reviews_count(self):
        return self.review_shop.count()

    def calculate_rating(self):
        
        return self.review_shop.aggregate(avg_rating = models.Avg('rating'))

    @property
    def components(self):
        return self.component_shop.filter(deleted=False, sold=False).count() or 0

    @property 
    def get_repaired_phones_count(self):
        return self.phone_shop.filter(todo__in=['r', 'f'], status='r').count() or 0
        # print 'property', j, self.name, 'repaired'
        # return j
    @property 
    def get_not_repaired_phones_count(self):
        return self.phone_shop.filter(todo__in=['r','u','f'], status='n').count() or 0
        # print 'property', j, self.name, 'not repaired'
        # return j

    @property 
    def get_unlocked_phones_count(self):
        return self.phone_shop.filter(todo='u', status='r').count() or 0
        # print 'property', j, self.name, 'unlocked'
        # return j

    @property 
    def get_satisfied_clients_count(self):
        return a_get_satisfied_clients_count(self)
        # print 'property', j, self.name, 'satisfied'
        # return j

class Invoices(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    method = models.CharField(choices=payment_choices,max_length=30)
    status = models.CharField(choices=(('PAID','PAID'),('UNPAID','UNPAID'),('REUPLOAD','REUPLOAD')),max_length=10,default='UNPAID')
    created = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop,blank=True,null=True)
    files_shop = models.ManyToManyField(SFileUpload,related_name='proof_shop_files')
    files_admin = models.ManyToManyField(SFileUpload,related_name='proof_admin_files')
    admin_comments = models.TextField(max_length=256,null=True,blank=True)
    sec_code = models.CharField(max_length=10,null=True,blank=True)
    proof_upload_date = models.DateTimeField(null=True,blank=True)


class InvoiceCharges(models.Model):
    invoice = models.ForeignKey(Invoices)
    charge_text = models.CharField(max_length=50)
    charge_amount = models.DecimalField(decimal_places=2,max_digits=6)


class Banner(models.Model):
    banner = VersatileImageField(upload_to='banners/')
    link = models.URLField()
    active = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return unicode(self.link)


class ShopManager(models.Manager):


    def get_shops_by_coords(self, latLng, ray=0.5):
        result_list = []
        latitude, longitude = map(latLng.split(','), int)
        max_west  = latitude - ray
        max_east  = latitude + ray
        max_north = longitude - ray
        max_south = longitude + ray
        shop_latitude, shop_longitude = self.location.split(',')
        if shop_latitude <= max_east and shop_latitude >=max_west:
            if shop_longitude <= max_south and shop_longitude >=max_north:
               result_list.append(shop)
        return result_list

class ActionHistory(models.Model):
    shop = models.ForeignKey(Shop)
    action = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

class BitcoinKeyInvoiceDict(models.Model):
    invoice = models.ForeignKey(Invoices)
    address = models.CharField(max_length=60)
    index = models.CharField(max_length=5)

class BitcoinHistory(models.Model):
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=60)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(null=True)
    invoice = models.ForeignKey(Invoices)
    key = models.ForeignKey(BitcoinKeyInvoiceDict,null=True)
    txhash = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=10,default='UNPAID')

