from django.db.models import ForeignKey, CharField, EmailField, TextField, URLField, DateTimeField, Model, BooleanField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

from app.server.models import Server
from app.shop.models import Shop

CHOICES = (('','--'),('admin', _('administrative')), ('tech',_('technical')), ('money',_('financial')))

class ContactAdmin(Model):
    user        = ForeignKey(User, related_name="sender" )
    subject     = CharField(max_length=255, default="Hello", blank=False, null=False )
    type        = CharField(max_length=5, blank=True, null=True, choices=CHOICES, default='')
    created_at  = DateTimeField(auto_now=True)
    message     = TextField(max_length=2048, blank=False, null=False)
    feedback    = TextField(max_length=2048, blank=True, null=True, default='')
    processed   = BooleanField(default=False)

    class Meta:
        verbose_name        = "Admin Contact"
        verbose_name_plural = "Admin Contacts"

    def __str__(self):
        return "{0}:{1}-{2}".format(self.user, self.type ,self.subject)

class KeyValueStore(Model):
    key  = TextField(null=False)
    title = CharField(max_length=60,null=False)
    category = CharField(max_length=30,blank=True,null=True)
    value =TextField(blank=True)
    active = BooleanField(default=True)

cat_choice = (('ADMINISTRATIVE','ADMINISTRATIVE'),('TECHNICAL','TECHNICAL'),('FINANCIAL','FINANCIAL'))
status_choice = (('OPEN','OPEN'),('SOLVED','SOLVED'))

class MessageThread(Model):
    subject = CharField(max_length=60)
    type = CharField(max_length=30,choices=cat_choice)
    active = BooleanField(default=True)
    status = CharField(max_length=30,choices=status_choice,default='OPEN')
    shop = ForeignKey(Shop,null=True,default=None)
    server = ForeignKey(Server,null=True,default=None)
    created_at = DateTimeField(auto_now_add=True)

    @property
    def first_message(self):
        return Message.objects.filter(thread=self).order_by('datetime').first()

class Message(Model):
    thread = ForeignKey(MessageThread)
    from_user = ForeignKey(User)
    message = TextField()
    datetime = DateTimeField(auto_now_add=True)

class AdminActionHistory(Model):
    action = CharField(max_length=100)
    created = DateTimeField(auto_now_add=True)
    user = ForeignKey(settings.AUTH_USER_MODEL)
    affected = TextField(blank=True,null=True)
