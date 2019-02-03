from __future__ import absolute_import
from django.conf.urls import patterns, url

from .views import (UpdateServerView, ServersListView, ServerPositionView, 
          ServerDetailView, DepositView, CreateServerView, ServerSearchView, addServerCredits,
                    serverCreditHistory)#  ServerFormSearchView, ,

urlpatterns = patterns('',
                       url(r'^$', ServersListView.as_view(), name='servers'),
                       # url(r'^search/$', 'app.server.views.search', name='search'),
                       url(r'^(?P<pk>[\d-]+)/(?P<slug>[\w-]+)/detail$', ServerDetailView.as_view(), name='server-detail'),
                       url(r'^deposit/$', DepositView.as_view(), name='server-deposit'),
                       url(r'^edit/$', UpdateServerView.as_view(),
                           name='server-edit'),
                       url(r'^create$', CreateServerView.as_view(), name='create-server'),
                       url(r'^position$', ServerPositionView.as_view(), name='server-position'),
                       url(r'^search/?$', ServerSearchView.as_view(), name='server-search'),
                       url(r'^addservercredits/$',addServerCredits,name='server-add-credits'),
                       url(r'^servercredithistory/$',serverCreditHistory,name='server-credit-history')
                       # url(r'^server-autocomplete/$', 'app.server.views.server_name_autocomplete', name='server-autocomplete'),
                       )
