# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import patterns, url
from .views import NotificationListView, NotificationHubView, markread_view, markread_bytype_view

CLIENT_REVIEW = 'L'
SHOP_REVIEW = 'C'
SERVER_REVIEW = 'F'
NEW_ORDER = 'T'
NEW_TICKET = 'A'
ORDER_CANCELED = 'W'
NEW_COMPONENT = 'E'
VALIDATE_ORDER_CANCELLING = 'S'
ORDER_CANCELLING_REFUSED = 'D'
ORDER_DONE = 'B'
ABUSE_REPORT_CONFIRMED = 'M'
AD_VALIDATE_ORDER_CANCELLING = 'S'
ABUSE_REPORT_DECLINED = 'K'
NEW_CLIENT_REQUEST = 'J'
INVOICE_PROOF_VERIFIED         = 'F'
INVOICE_PROOF_REUPLOAD         = 'P'
# TICKET_CLOSED = 'H'
# AD_CHATTING = 'I'
# TAGGED      = 'Z'
ADMIN_RESPONSE = 'I'  # 10
SERVER_RESPONSE = 'Z'  # 11
NO_SERVER_RESPONSE_SERVER = 'Q'
NO_SERVER_RESPONSE_SHOP = 'N'
ACCEPTED_TRANSACTION = 'W'  # 12
TRANSACTION_DECLINED = 'M'  # 13
NEW_BRAND_ADDED              = 'K' # 14
NEW_MODEL_ADDED              = 'B' # 15

CLIENT_STATUS_CHANGED        = "G" # 17
CLIENT_PAID_FOR_AT           = "P" # 18

CLIENT_HAS_TO_REVIEW = 'H'
ORDER_DELIVERY_TIME_EXCEEDED = 'Y' # 6
ORDER_DELIVERY_TIME_IS_CLOSE = 'D' # 7
ORDER_DELIVERED = 'S'  # 5
urlpatterns = patterns('',
	url(r'^invoices$',NotificationListView.as_view(type=[INVOICE_PROOF_REUPLOAD,INVOICE_PROOF_VERIFIED,],template_name = "urpsm/v2/notifications/invoice_notifications_list_v2.html"), name='invoice-notification'),
	url(r'^clients$', NotificationListView.as_view(type=[CLIENT_STATUS_CHANGED, CLIENT_PAID_FOR_AT], template_name = "urpsm/v2/notifications/client_notifications_list_v2.html"), name='client-notification'),
	url(r'^reviews$', NotificationListView.as_view(type=[CLIENT_REVIEW, SHOP_REVIEW, SERVER_REVIEW, CLIENT_HAS_TO_REVIEW], template_name = "urpsm/v2/notifications/review_notifications_list_v2.html"), name='review-notification'),
	url(r'^payments$', NotificationListView.as_view(type=[ACCEPTED_TRANSACTION, TRANSACTION_DECLINED], template_name = "urpsm/v2/notifications/payment_notifications_list_v2.html"), name='payment-notification'),
	url(r'^phones$', NotificationListView.as_view(type=[NEW_BRAND_ADDED,NEW_MODEL_ADDED], template_name = "urpsm/v2/notifications/phone_notifications_list_v2.html"), name='phone-notification'),
	url(r'^components$', NotificationListView.as_view(type=[NEW_COMPONENT], template_name = "urpsm/v2/notifications/component_notifications_list_v2.html"), name='component-notification'),
	url(r'^orders$', NotificationListView.as_view(type=[ORDER_DONE, NEW_ORDER, VALIDATE_ORDER_CANCELLING, ORDER_CANCELLING_REFUSED, ORDER_CANCELED,ORDER_DELIVERY_TIME_EXCEEDED,ORDER_DELIVERY_TIME_IS_CLOSE,ORDER_DELIVERED], template_name = "urpsm/v2/notifications/order_notifications_list_v2.html"), name='order-notification'),
	url(r'^tickets$', NotificationListView.as_view(type=[NEW_TICKET, ADMIN_RESPONSE,SERVER_RESPONSE], template_name = "urpsm/v2/notifications/ticket_notifications_list_v2.html"), name='ticket-notification'),
	url(r'^administration$', NotificationListView.as_view(type=[NEW_CLIENT_REQUEST], template_name = "urpsm/v2/notifications/admin_notifications_list_v2.html"), name='admin-notification'),
	url(r'^hub$', NotificationHubView.as_view(), name='notifications-hub'),
    url(r'^last/$', 'app.notifications.views.last_notifications', name='last_notifications'),
    url(r'^check/$', 'app.notifications.views.check_notifications', name='check_notifications'),
    url(r'^send/$', 'app.notifications.views.send_notification', name='send-notification'),
	url(r'^markreadtype/$',markread_bytype_view,name='markread-bytype'),
	url(r'^markread/$',markread_view,name='markread'),
   )