from __builtin__ import unicode
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags
from app.shop.models import Shop, Invoices
from app.server.models import Server
from app.component.models import Component
from app.order.models import ServerOrder
from app.client.models import Client
from app.ticket.models import OrderTicket
from app.phone.models import Brand, Model
from app.ureview.models import ShopReview, ServerReview
from app.payment.models import ServerPaymentTransaction
from django.contrib.auth.models import Group

GROUPS = Group.objects.all()

# for group in GROUPS:
#     if group.name == 'Administrator':
#         ADMINISTRATOR = group
#     if group.name ==  'Technician':
#         TECHNICIAN = group
#     if group.name ==  'Worker':
#         WORKER = group

ADMINISTRATOR = TECHNICIAN = WORKER = None


#ABCDEFGHIJKLMNOPQRSTUVWXYZ
#ABCDEFGHIJKLMNOPQ ST  W YZ
class Notification(models.Model):
    #review
    NEW_CLIENT_REVIEW            = 'L' # 1
    NEW_SHOP_REVIEW              = 'C' #2 
    #SERVER_REVIEW                = 'F'
    CLIENT_HAS_TO_REVIEW         = 'H' #3
    REVIEW_WHO_TO_NOTIFY         = {'server':[NEW_SHOP_REVIEW], 'shop':[NEW_CLIENT_REVIEW,CLIENT_HAS_TO_REVIEW]}
    REVIEW_GROUPS_TO_NOTIFY      = [ADMINISTRATOR, TECHNICIAN, WORKER]
    #order
    NEW_ORDER                    = 'T' # 4
    ORDER_DELIVERED              = 'S' # 5
    ORDER_DELIVERY_TIME_EXCEEDED = 'Y' # 6
    ORDER_DELIVERY_TIME_IS_CLOSE = 'D' # 7
    ORDER_CANCELLED              = 'O' # 7
    ORDER_WHO_TO_NOTIFY         = {'server':[ORDER_DELIVERY_TIME_IS_CLOSE, NEW_ORDER, ORDER_DELIVERED, ORDER_DELIVERY_TIME_EXCEEDED ], 'shop':[ORDER_DELIVERED, ORDER_DELIVERY_TIME_EXCEEDED]}
    ORDER_GROUPS_TO_NOTIFY       = [ADMINISTRATOR, TECHNICIAN]
    #component
    NEW_COMPONENT                = 'E' # 8
    COMPONENT_WHO_TO_NOTIFY      = {'server':[NEW_COMPONENT ], 'shop':[NEW_COMPONENT]}
    COMPONENT_GROUPS_TO_NOTIFY   = [ADMINISTRATOR, TECHNICIAN]
    #ticket
    NEW_TICKET                   = 'A' # 9
    ADMIN_RESPONSE               = 'I' # 10
    SERVER_RESPONSE              = 'Z' # 11 
    NO_SERVER_RESPONSE_SERVER    = 'Q'
    NO_SERVER_RESPONSE_SHOP      = 'N'
    TICKET_WHO_TO_NOTIFY         = {'server':[NEW_TICKET, ADMIN_RESPONSE], 'shop':[ADMIN_RESPONSE,SERVER_RESPONSE]}
    TICKET_GROUPS_TO_NOTIFY      = [ADMINISTRATOR, TECHNICIAN]
    #payment
    ACCEPTED_TRANSACTION         = 'W' # 12
    TRANSACTION_DECLINED         = 'M' # 13
    PAYMENT_WHO_TO_NOTIFY         = {'server':[ACCEPTED_TRANSACTION, TRANSACTION_DECLINED], 'shop':[]}
    PAYMENT_GROUPS_TO_NOTIFY     = [ADMINISTRATOR]
    #phone
    NEW_BRAND_ADDED              = 'K' # 14
    NEW_MODEL_ADDED              = 'B' # 15 
    PHONE_WHO_TO_NOTIFY          = {'server':[NEW_BRAND_ADDED,NEW_MODEL_ADDED], 'shop':[NEW_BRAND_ADDED,NEW_MODEL_ADDED]}
    PHONE_GROUPS_TO_NOTIFY       = [ADMINISTRATOR, TECHNICIAN, WORKER]
    #admin 
    ADMIN_NOTIF                  = 'J' # 16
    ADMIN_WHO_TO_NOTIFY          = {'server':[ADMIN_NOTIF], 'shop':[ADMIN_NOTIF]}
    ADMIN_GROUPS_TO_NOTIFY       = [ADMINISTRATOR, TECHNICIAN]
    #client
    CLIENT_STATUS_CHANGED        = "G" # 17
    CLIENT_PAID_FOR_AT           = "P" # 18
    CLIENT_WHO_TO_NOTIFY          = {'server':[], 'shop':[CLIENT_STATUS_CHANGED, CLIENT_PAID_FOR_AT]}
    CLIENT_GROUPS_TO_NOTIFY      = [ADMINISTRATOR, TECHNICIAN, WORKER]

    INVOICE_PROOF_VERIFIED         = 'F'
    INVOICE_PROOF_REUPLOAD         = 'P'
    INVOICE_WHO_TO_NOTIFY          ={'server':[],'shop':[INVOICE_PROOF_VERIFIED,INVOICE_PROOF_REUPLOAD]}
    MESSAGE_USER = 'R'

    MESSAGE_USER_WHO_TO_NOTIFY = {'server':[MESSAGE_USER],'shop':[MESSAGE_USER]}


    NOTIFICATION_TYPES = (
        #review
        (NEW_CLIENT_REVIEW, _('new review from client') ),                        ## 1
        (NEW_SHOP_REVIEW, _('new shop review') ),                                 ## 2
        (CLIENT_HAS_TO_REVIEW, _('client has to review') ),                       ## 3
        #order
        (NEW_ORDER, _('new order') ),                                             ## 4
        (ORDER_DELIVERED, _('an order has been delivered')),                      ## 5
        (ORDER_DELIVERY_TIME_EXCEEDED, _('an order has exceeded delivery time')), ## 6
        (ORDER_DELIVERY_TIME_IS_CLOSE, _('order cancelling refused')),            ## 7
        #component
        (NEW_COMPONENT, _('new component')),                                      ## 8
        #ticket
        (NEW_TICKET, _('new ticket')),                                            ## 9
        (ADMIN_RESPONSE, _('admin has responded to your ticket') ),               ## 10
        (SERVER_RESPONSE, _('server has responded to you ticket') ),              ## 11
        (NO_SERVER_RESPONSE_SERVER, _('your did not respond to ticket within 3 days, order will be canceled') ),              ## 11
        (NO_SERVER_RESPONSE_SHOP, _('unlocking server did not respond to your ticket within 3 days, you will be refunded.') ),              ## 11
        #payment
        (ACCEPTED_TRANSACTION, _('payment transaction accepted')),                ## 12
        (TRANSACTION_DECLINED, _('payment transaction declined')),                ## 13
        #phone
        (NEW_BRAND_ADDED, _('new brand added')),                                  ## 14
        (NEW_MODEL_ADDED, _('new model added')),                                  ## 15
        #admin
        (ADMIN_NOTIF, _('admin notification')),                                   ## 16
        #client
        (CLIENT_STATUS_CHANGED, _('client status has been changed') ),            ## 17
        (CLIENT_PAID_FOR_AT, _('client status has been paid') ),
        (INVOICE_PROOF_REUPLOAD,_('proof was rejected. please re-upload')),       ## 18
        (INVOICE_PROOF_VERIFIED,_('proof verified. funds added to account')),
        (MESSAGE_USER,_('Received a new message'))## 19

        )

    #review
    _NEW_CLIENT_REVIEW_TEMPLATE = "you've got a client review"
    _NEW_SHOP_REVIEW_TEMPLATE = "you've got a shop review"
    _CLIENT_HAS_TO_REVIEW_TEMPLATE = "a client has to review"
    #admin
    _ADMIN_NOTIF_TEMPLATE = "you've got a new client request"
    #order
    _NEW_ORDER_TEMPLATE = "you've got a new order"
    _ORDER_DELIVERED_TEMPLATE = "order is done"
    _ORDER_DELIVERY_TIME_IS_CLOSE_TEMPLATE = "an order cancellation refused"
    _ORDER_DELIVERY_TIME_EXCEEDED_TEMPLATE = "an order has exceeded delivery time"
    _ORDER_CANCELLED_TEMPLATE = "order has been cancelled"
    #component
    _NEW_COMPONENT_TEMPLATE   = _("a new component")
    #ticket
    _NEW_TICKET_TEMPLATE      = "you've got a new ticket"
    _ADMIN_RESPONSE_TEMPLATE  = mark_safe('<a href="/en/profile/{0}">{1}</a> wants to discuss with you about <strong>{2}</strong>&nbsp;&nbsp;&nbsp;<a href="/en/messages/chat/{0}/about/{3}/{4}/">Go to chat</a>')
    _SERVER_RESPONSE_TEMPLATE = mark_safe("<a href='/en/profile/{0}'>{1}</a> tagged you on one of his feed: <a href='/en/feeds/{2}/'></a>")
    _NO_SERVER_RESPONSE_SERVER_TEMPLATE  =  "you did not answer on this raised ticket {0} within 3 days, order {1} will be canceled."
    _NO_SERVER_RESPONSE_SHOP_TEMPLATE  =  "unlocking server {0} did not answer on your raised ticket {1} within 3 days, you will be refunded."
    #payment
    _ACCEPTED_TRANSACTION_TEMPLATE = "your payment transaction is accepted"
    _TRANSACTION_DECLINED_TEMPLATE = "your payment transaction has been declined"
    #phone
    _NEW_BRAND_ADDED_TEMPLATE = "a new brand {0} is added"
    _NEW_MODEL_ADDED_TEMPLATE = "a new model {0} {1} has been added"
    #client
    _CLIENT_STATUS_CHANGED_TEMPLATE= 'the client {0} status has been changed at {1}' # 0: user , 1: client ref, 2: updated
    _CLIENT_PAID_FOR_AT_TEMPLATE   = 'the client {0} has been paid to {1} at {2}' # 0: user , 1: client ref, 2: updated
    #invoice
    _INVOICE_PROOF_REUPLOAD_TEMPLATE = 'proof for invoice {0} was rejected. please re-upload'
    _INVOICE_PROOF_VERIFIED_TEMPLATE =  'proof for invoice {0} was verified. funds added to account'

    shop              = models.ForeignKey(Shop,        related_name='notif_shop',      null=True, blank=True)
    server            = models.ForeignKey(Server,      related_name='notif_server',    null=True, blank=True)
    server_order      = models.ForeignKey(ServerOrder, related_name='notif_order',     null=True, blank=True)
    client            = models.ForeignKey(Client,      related_name='notif_client',    null=True, blank=True)
    ticket            = models.ForeignKey(OrderTicket, related_name='notif_ticket',    null=True, blank=True)
    component         = models.ForeignKey(Component,   related_name='notif_component', null=True, blank=True)
    payment           = models.ForeignKey(ServerPaymentTransaction,   related_name='notif_payment', null=True, blank=True)
    server_review     = models.ForeignKey(ServerReview,related_name='notif_server_review', null=True, blank=True)
    shop_review       = models.ForeignKey(ShopReview,  related_name='notif_shop_review', null=True, blank=True)
    brand             = models.ForeignKey(Brand,       related_name='notif_brand',     null=True, blank=True)
    model             = models.ForeignKey(Model,       related_name='notif_model',     null=True, blank=True)
    from_user         = models.ForeignKey(User,        related_name='notif_sender',    null=True, blank=True)
    to_user           = models.ForeignKey(User,        related_name='notif_recepient', null=True, blank=True)
    date              = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read           = models.BooleanField(default=False)
    message           = models.TextField(blank=True, null=True, default='')
    invoice           = models.ForeignKey(Invoices,    related_name="notif_invoice",    null=True,blank=True)

    # brand             = models.ForeignKey(OrderTicket, related_name='notif_brand',     null=True, blank=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def strng(self):
        return self.__unicode__()

    @property
    def get_review(self):
        return ShopReview.objects.get(client=self.client)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self.notification_type == self.MESSAGE_USER:
            return "You have got a new meesage"
        try:
            if self.notification_type == self.NEW_CLIENT_REVIEW:
                return self._NEW_CLIENT_REVIEW_TEMPLATE
                # return _(self._LIKED_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     self.feed.pk,
                #     strip_tags(self.get_summary(self.feed.post))
                #     )
            if self.notification_type == self.NEW_SHOP_REVIEW:
                return self._NEW_SHOP_REVIEW_TEMPLATE
                # return _(self._AD_ADDED_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     self.ad.pk,
                #     escape(self.get_summary(self.ad.title))
                #     )
            if self.notification_type == self.NEW_ORDER:
                return self._NEW_ORDER_TEMPLATE
                # return _(self._AD_LIKED_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     self.ad.pk,
                #     escape(self.get_summary(self.ad.title))
                #     )
            if self.notification_type==self.NEW_BRAND_ADDED:
                return _(self._NEW_BRAND_ADDED_TEMPLATE).format(
                        escape(self.brand)
                    )
            if self.notification_type==self.NEW_MODEL_ADDED:
                return _(self._NEW_MODEL_ADDED_TEMPLATE).format(
                        escape(self.brand),
                        escape(self.model),
                    )

            elif self.notification_type == self.CLIENT_STATUS_CHANGED:
                # return self._CLIENT_PAID_FOR_AT_TEMPLATE
                try:
                    return _(self._CLIENT_STATUS_CHANGED_TEMPLATE).format(
                        escape(self.client.ref),
                        escape(self.to_user),
                        escape(self.client.updated)
                        )
                except:return self._CLIENT_STATUS_CHANGED_TEMPLATE

            elif self.notification_type == self.CLIENT_PAID_FOR_AT:
                # return self._CLIENT_PAID_FOR_AT_TEMPLATE
                try:
                    return _(self._CLIENT_PAID_FOR_AT_TEMPLATE).format(
                        escape(self.client.ref),
                        escape(self.client.paid_to),
                        escape(self.client.updated)
                        )
                except:return self._CLIENT_PAID_FOR_AT_TEMPLATE
            elif self.notification_type == self.NEW_TICKET:
                return self._NEW_TICKET_TEMPLATE
                # return _(self._AD_COMMENTED_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     self.ad.pk,
                #     escape(self.get_summary(self.ad.title))
                #     )
            elif self.notification_type == self.ACCEPTED_TRANSACTION:
                return self._ACCEPTED_TRANSACTION_TEMPLATE 
                # return _(self._COMMENTED_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     self.feed.pk,
                #     self.get_summary(strip_tags(self.feed.post))
                #     )
            elif self.notification_type == self.ADMIN_NOTIF:
                return self._ADMIN_NOTIF_TEMPLATE
                # return _(self._EDITED_ARTICLE_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     self.article.slug,
                #     escape(self.get_summary(self.article.title))
                #     )
            elif self.notification_type == self.NEW_COMPONENT:
                return self._NEW_COMPONENT_TEMPLATE
                # return _(self._ALSO_COMMENTED_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     self.feed.pk,
                #     self.get_summary(escape(self.feed.post))
                #     )
            elif self.notification_type == self.VALIDATE_ORDER_CANCELLING:
                return self._VALIDATE_ORDER_CANCELLING_TEMPLATE
                # return _(self._IS_FOLLOWING_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name())
                #     )
            elif self.notification_type == self.ORDER_DELIVERY_TIME_IS_CLOSE:
                return self._ORDER_DELIVERY_TIME_IS_CLOSE_TEMPLATE
                # return _(self._NOT_FOLLOWING_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name())
                #     )
            elif self.notification_type == self.ORDER_DELIVERED:
                return self._ORDER_DELIVERED_TEMPLATE
                # return _(self._CHATTING_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name())
                #     )
            elif self.notification_type == self.TRANSACTION_DECLINED:
                return self._TRANSACTION_DECLINED_TEMPLATE
                # return _(self._ADMIN_RESPONSE_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name()),
                #     escape(self.ad.title),
                #     escape(self.ad.slug),
                #     escape(self.ad.id)
                #     )
            elif self.notification_type == self.ORDER_DELIVERY_TIME_EXCEEDED:
                return self._ORDER_DELIVERY_TIME_EXCEEDED
                # return _(self._LEAVING_CHAT_TEMPLATE).format(
                #     escape(self.from_user.username),
                #     escape(self.from_user.profile.get_screen_name())
                #     )
            elif self.notification_type == self.NEW_BRAND_ADDED:
                return self._NEW_BRAND_ADDED

            elif self.notification_type == self.ORDER_CANCELLED:
                return self._ORDER_CANCELLED_TEMPLATE

            elif self.notification_type == self.NO_SERVER_RESPONSE_SERVER:
                return self._NO_SERVER_RESPONSE_SERVER_TEMPLATE.format(
                    escape(self.ticket.ref),
                    escape(self.ticket.server_order.ref),
                    )
            elif self.notification_type == self.NO_SERVER_RESPONSE_SHOP:
                return self._NO_SERVER_RESPONSE_SHOP_TEMPLATE.format(
                    escape(self.server),
                    escape(self.ticket)
                    )
            elif self.notification_type == self.NEW_SHOP_REVIEW:
                return self._NEW_SHOP_REVIEW_TEMPLATE.format(
                    escape(self.shop.pk),
                    )
            elif self.notification_type == self.SERVER_REVIEW:
                return self._SERVER_REVIEW_TEMPLATE.format(
                    escape(self.server.pk),
                    )
            elif self.notification_type == self.INVOICE_PROOF_VERIFIED:
                return "proof was verified. funds added"
            elif self.notification_type == self.INVOICE_PROOF_REUPLOAD:
                return "proof was rejected. please re-upload"
            else:
                return ""
        except:
            return _('Ooops! Something went wrong.')

    def get_summary(self, value=''):
        summary_size = 50

        if value and len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value

    def __str__(self):
        return __unicode__(self)