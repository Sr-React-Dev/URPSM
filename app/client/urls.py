# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import patterns, url

from .views import (CreateClientView, ClientsView, QRTicketView, PaidClientView,
                    UpdateClientView, DeleteClientView, DetailClientView, ClientReviewView)

urlpatterns = patterns('',
                       url(r'^$', ClientsView.as_view(),
                           name='clients'),
                       url(r'^redactor/image/$',
                           'app.client.views.redactor_image', name='redactor_image'),
                       url(r'^create/$', CreateClientView.as_view(),
                           name='client-create'),
                       url(r'^(?P<pk>\d+)/ticket/$',
                           QRTicketView.as_view(), name='client-ticket'),
                       url(r'^(?P<pk>\d+)/update/$',
                           UpdateClientView.as_view(), name='client-update'),
                       url(r'^(?P<uuid>[^/]+)/status/$',
                           ClientReviewView.as_view(), name='client-qr'),
                       url(r'^(?P<pk>\d+)/delete/$',
                           DeleteClientView.as_view(), name='client-delete'),
                       url(r'^(?P<pk>\d+)/paid/$',
                           PaidClientView.as_view(), name='client-paid'),
                       url(r'^paid/$',
                           PaidClientView.as_view(), name='client-paid-ajax'),
                       url(r'^detail/$', DetailClientView.as_view(),
                           name='client-detail')
                       )
