from __future__ import absolute_import
from django.conf.urls import patterns, url

from .views import (Dash, ServerDash, ShopPositionView, ContactAdminView, AdminThankYouView, server_sales_dash,
                    newContactAdminView, message_thread)

urlpatterns = patterns('',
                       url(r'^shop-dashboard$', Dash.as_view(), name='dash'),
                       url(r'^server-dashboard$', ServerDash.as_view(), name='server-dash'),
                       url(r'^server-sales-dashbaord',server_sales_dash,name='sales-dashboard'),
                       url(r'^shop/postion/$', ShopPositionView.as_view(), name='shop-position'),
                       url(r'^contact/admin/$', newContactAdminView, name='contact-admin'),
                       url(r'^messages/(?P<id>\d+)/$',message_thread,name='message-thread'),
                       url(r'^contact/admin/thankyou$', AdminThankYouView.as_view(template_name="urpsm/v2/dash/admin_thankyou_v2.html"), name='adminthankyou'),
                       url(r'^send-feedback$', 'app.dash.views.send_feedback', name='manager-send-feedback'),
                       )
