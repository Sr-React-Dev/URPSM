# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import patterns, url
from .views import (CreateComponentView, ComponentView, UpdateComponentView, DeleteComponentView,
   ComponentDetailView, ComponentListView, ComponentSearchView, )

urlpatterns = patterns('',
                       url(r'^$', ComponentView.as_view(),
                           name='components'),
                       url(r'^add/$', CreateComponentView.as_view(),
                           name='component-create'),
                       url(r'^(?P<pk>\d+)/edit/$',
                           UpdateComponentView.as_view(), name='component-edit'),
                       url(r'^(?P<pk>\d+)/delete/$',
                           DeleteComponentView.as_view(), name='component-delete'),
                       url(r'^search/?$', ComponentSearchView.as_view(), name='components-search'),
                       url(r'^shops-components/?$', ComponentListView.as_view(), name='components-list'),
                       url(r'^(?P<pk>[\d-]+)/(?P<slug>[\w-]+)/detail$', ComponentDetailView.as_view(), name='component-detail'),
                       )
