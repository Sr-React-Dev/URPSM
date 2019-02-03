# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from app.notifications.models import Notification
from app.shop.models import Shop
from app.server.models import Server
from .utils import get_key, mailer
from .managers import ProfileManager
email_template = "urpsm/notifications/email_notifications.html"

@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_(u'User'), related_name=_(u'profile'), primary_key=True)
    shop = models.ForeignKey(
        Shop, related_name='user_shop', null=True, blank=True)
    server = models.ForeignKey(
        Server, related_name='user_server', null=True, blank=True)
    phone = PhoneNumberField(
        help_text='eg: +212612345678', blank=True, null=True)
    # address = models.TextField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    activation_key = models.CharField(
        _(u'Activation key'), max_length=64, blank=True)
    unconfirmed_email = models.EmailField(_(u'Unconfirmed email'), blank=True)
    email_confirmation_key = models.CharField(
        _(u'New email verification key'), max_length=64, blank=True)
    block_access = models.BooleanField(default=False)
    has_business  = models.BooleanField(default=False)
    has_to_review = models.BooleanField(default=False)
    ip_address    = models.CharField(_('current ip'), max_length=40, blank=True, null=True)
    remote_addr    = models.TextField(blank=True, null=True)
    objects = ProfileManager()

    class Meta:
        verbose_name = _(u'Profile')
        verbose_name_plural = _(u'Profiles')

    def __str__(self):
        return unicode(self.user.username)

    def activation_email(self):
        to = self.user.email
        subject = _(u'Account activation')
        ctx = {
            'activation_key': self.activation_key,
        }
        mailer(template_name='urpsm/accounts/emails/activation_email.html',
               subject=subject, recipient=to, ctx=ctx)

    def change_email(self, new_email):
        self.unconfirmed_email = new_email
        self.email_confirmation_key = get_key()
        self.save()
        self.email_confirmation()

    def email_confirmation(self):
        to = self.unconfirmed_email
        subject = 'Email confirmation'
        ctx = {
            'confirmation_key': self.email_confirmation_key,
        }
        mailer(template_name='urpsm/accounts/emails/new_email_confirmation.html',
               subject=subject, recipient=to, ctx=ctx)
    #Reviews notification 
    def notify_new_client_review(self, shop, client):
        Notification(notification_type=Notification.NEW_CLIENT_REVIEW, shop=shop, client=client).save()

    def notify_new_shop_review(self, server, shop):
        Notification(notification_type=Notification.NEW_SHOP_REVIEW, shop=shop, server=server).save()
    def notify_client_has_to_review(self, shop, client):
        Notification(notification_type=Notification.CLIENT_HAS_TO_REVIEW, shop=shop, client=client).save()
    #ServerOrder notification
    def notify_server_for_new_order(self, server, shop, order):
        Notification(notification_type=Notification.NEW_ORDER, shop=shop, server=server, server_order=order)

    def notify_order_delivered(self, server, order, shop):
        Notification(notification_type=Notification.ORDER_DELIVERED, shop=shop, server=server, server_order=order).save()

    def notify_order_delivery_time_close(self, server, order):
        Notification(notification_type=Notification.ORDER_DELIVERY_TIME_IS_CLOSE, server=server, server_order=order).save()
    def notify_order_delivery_time_exceeded(self, server,shop, order):
        Notification(notification_type=Notification.ORDER_DELIVERY_TIME_EXCEEDED,  shop=shop, server=server, server_order=order).save()
    def notifiy_order_cancelled(self, server, shop, order):
        Notification(notification_type=Notification.ORDER_CANCELLED,  shop=shop, server=server, server_order=order).save()



    #ticket notification
    def notify_new_ticket(self, shop, server, ticket):
        Notification(notification_type=Notification.NEW_TICKET, shop=shop, server=server, ticket=ticket).save()
    def notify_server_response(self, shop, server, ticket):
        Notification(notification_type=Notification.SERVER_RESPONSE, shop=shop, server=server, ticket=ticket).save()
    def notify_admin_response(self, shop, server, ticket):
        Notification(notification_type=Notification.ADMIN_RESPONSE, shop=shop, server=server, ticket=ticket).save()
    def notify_no_server_response_server(self, order, server, ticket):
        Notification(notification_type=Notification.NO_SERVER_RESPONSE_SERVER, server_order=order, server=server, ticket=ticket)

    def notify_no_server_response_shop(self, order, shop, ticket):
        Notification(notification_type=Notification.NO_SERVER_RESPONSE_SHOP, server_order=order, shop=shop, ticket=ticket).save()
    #PAYMENT NOTIFICATION
    def notify_accepted_transaction(self, server, payment=False):
        Notification(notification_type=Notification.ACCEPTED_TRANSACTION, server=server).save()
    def notify_declined_transaction(self, server, payment):
        Notification(notification_type=Notification.TRANSACTION_DECLINED, shop=shop, payment=payment).save()
    #phone notificatin
    def notify_new_brand(self, brand):
        Notification(notification_type=Notification.NEW_BRAND_ADDED, brand=brand).save()
    def notify_new_model(self, model):
        Notification(notification_type=Notification.NEW_MODEL_ADDED, model=model).save()
    #admin notification
    def notify_shop_by_admin(self, shop, message):
        Notification(notification_type=Notification.ADMIN_NOTIF, shop=shop, message=message).save()
    def notify_server_by_admin(self, server, message):
        Notification(notification_type=Notification.ADMIN_NOTIF, server=server, message=message).save()
    #client notification
    def notify_client_status_changed(self, shop, client, changer):
        if self.user.profile.shop==shop:
            try:
                if self.user.groups.all()[0] in Notification.CLIENT_GROUPS_TO_NOTIFY:
                    Notification(notification_type=Notification.CLIENT_STATUS_CHANGED, shop=shop, client=client, to_user=changer).save()
            except:pass
    def notify_client_paid_for_at(self, shop, client, cashierman ):
        if self.user.profile.shop==shop and not self.user==cashierman:
            try:
                if self.user.groups.all()[0] in Notification.CLIENT_GROUPS_TO_NOTIFY:
                    Notification(notification_type=Notification.CLIENT_PAID_FOR_AT, shop=shop, client=client, to_user=cashierman).save()
            except:pass


        

        






   










    def save(self, *args, **kwargs):
        if not self.activation_key:
            self.activation_key = get_key()
        super(Profile, self).save(*args, **kwargs)
