from __future__ import absolute_import
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^transfer_money_from_wallet/$',
                           'app.payment.views.transfer_money_from_wallet')
                       )
