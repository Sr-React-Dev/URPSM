from __future__ import absolute_import
from django.conf.urls import patterns, url

from app.ureview.views import create_server_order_review
from .views import UnlockingView, ServerOrdersView, ServiceDown, ServerOrderDetailView, CancelServerOrderView, ServerOrderTicketsListView, \
    UnlockingViewF

urlpatterns = patterns('',
                       url(r'^$', ServerOrdersView.as_view(),
                           name='orders'),
                       url(r'^servicebusy/$', ServiceDown.as_view(),
                           name='servicebusy'),
                       url(r'^create/$', UnlockingViewF,
                           name='unlocking'),
                       url(r'^(?P<pk>\d+)/detail/$',
                           ServerOrderDetailView.as_view(), name='order-detail'),
                       url(r'^(?P<pk>\d+)/cancel/$',
                           CancelServerOrderView.as_view(), name='cancel-order'),
                       url(r'^tickets/', ServerOrderTicketsListView.as_view(), name="order-tickets"),
                       url(r'^review', create_server_order_review, name='server-order-review'),
                       # url(r'^(?P<order_id>\d+)/cancel-order/$',
                       #     cancel_server_order,
                       #     name="cancel_server_order"),
                       )
