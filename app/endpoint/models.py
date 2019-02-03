from __future__ import absolute_import
from django.db import models
from app.dhrufusion.client import Client as DhruClient
from app.nakshfusion.client import Client as NakshClient
from app.nakshfusion.gsm_client import Client as GsmClient
from app.shop.models import Shop
from app.server.models import Server
from app.search.index import Indexed, SearchField, FilterField, RelatedFields
from django.utils.translation import ugettext_lazy as _

def get_providers():
    return ( ('',''), ('dhru', 'DHRU'), ('naksh', 'Naksh Soft'),('gsm','Gsm Genie') )



class Network(models.Model):
    name = models.CharField(max_length=255)
    services = models.TextField()  # can pass attributes like null, blank, etc.
    
    def __str__(self):
        return unicode(self.name)

class Endpoint(models.Model, Indexed):
    server   = models.ForeignKey(Server, null=True, related_name="server_endpoint")
    url      = models.URLField(unique=True)
    username = models.CharField(max_length=255)
    key      = models.CharField(max_length=255)
    networks = models.ManyToManyField(Network, blank=True, default=None)
    provider = models.CharField(max_length=16, choices=get_providers(), blank=False, null=False, default='dhru')
    active   = models.BooleanField(default=False)

    def __str__(self):
        return "%s endpoint" % unicode(self.server.name)

    def delete(self, using=None, keep_parents=False):
        self.active = False
        self.save()
    
    # @property 
    def get_client(self):
        client = 'None'
        if self.provider == 'dhru':
            client = DhruClient(username=self.username, apiaccesskey=self.key,
                   dhrufusion_url=self.url)
        elif self.provider == 'naksh':
            client = NakshClient(userId=self.username, apiKey=self.key,
                    nakshfusion_url=self.url)
        elif self.provider == 'gsm':
            client = GsmClient(userId=self.username, apiKey=self.key,
                                 gsm_url=self.url,server=self.server)
        return client

    def get_credit(self):
        client = 'None'
        if self.provider == 'dhru':
            credit = self.client.get_credit()
        elif self.provider == 'naksh' or self.provider == 'gsm':
            credit = self.server.credit
        return credit
    
    client = property(get_client)
    credit = property(get_credit)

    @property
    def status(self):
        try:
            c = self.client.status()
            return c
        except: return False

    def account_info(self):
        if self.status:
            c = self.client
            if c:
                return c.get_credit()
        return False

    def service_info(self, id=None):
        if self.status:
            c = self.client
            if c:   
                return c.get_imei_service_details(id=id)
        return False

    def service_info_new(self,id):
        if self.status:
            c = self.client
            if c:
                return c.get_imei_service_detail_new(id=id)
        return None

    def place_order(self, service_id, imei):
        if self.status:
            c = self.client
            if c:
                return c.place_imei_order(service_id, imei)
        return False

    def order_info(self, id):
        if self.status:
            c = self.client
            if c:
                return c.get_imei_order(id)
        return False

    def get_networks_count(self):
        return self.networks.count()

    search_fields = [
        FilterField('active'),
        SearchField('url'),
        SearchField('provider'),
        RelatedFields('networks', [
            SearchField('name', partial_match=True, boost=10),
            SearchField('services', partial_match=True, boost=10),
        ]),
        RelatedFields('server', [
            SearchField('name', partial_match=True, boost=10),
            SearchField('slug', partial_match=True, boost=10),
            SearchField('description', partial_match=True, boost=10),
            SearchField('address'),
            SearchField('website'),
            SearchField('twitter'),
            SearchField('facebook'),
            SearchField('google_plus'),
            FilterField('blocked'),
            FilterField('created'),
            FilterField('level'),
            FilterField('rank'),
            FilterField('performance'),
            FilterField('average_rating'),
        ]),
        ]

    class Meta:
        unique_together = (('url',),)



