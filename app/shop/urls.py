from __future__ import absolute_import
from django.conf.urls import patterns, url

from .views import (UpdateShopView, ShopsListView, ShopDetailView, shop_invoices,
                    ComponentDetail, DepositView, CreateShopView, ShopSearchView, PublicShopSearchView,
                    shop_proof_invoice, generate_invoice, action_history,bitcoin_callback)  #, CreateShopView

urlpatterns = patterns('',
                       url(r'^$', ShopsListView.as_view(), name='shop'),
                       # url(r'', ShopsListView.as_view(), name='shop'),
                       # url(r'^search/$', 'app.shop.views.search', name='search'),
                       url(r'^invoices/$',shop_invoices,name='shop-invoices'),
                       url(r'^actionhistory/$', action_history, name='action-history'),
                       url(r'^invoices/(?P<pk>\d+)/$',shop_proof_invoice,name='proof-upload'),
                       url(r'^confirm-bitcoin-payment/(?P<invoice>\d+)/(?P<secret>\w+)/$',bitcoin_callback,name="bitcoin-callback"),
                       url(r'^search/$', ShopSearchView.as_view(), name='shop-search'),
                       url(r'^country-search/', PublicShopSearchView.as_view(), name='search-shops'),
                       url(r'^deposit/$', DepositView.as_view(), name='deposit'),
                       url(r'^edit/$', UpdateShopView.as_view(),
                           name='shop-edit'),
                       url(r'^generate_invoice/(?P<pk>\d+)/invoice.pdf$',generate_invoice,name='generate-invoice'),
                       url(r'^(?P<slug>[\w-]+)/$', ShopDetailView.as_view(), name='shop-detail'),
                       url(r'^create$', CreateShopView.as_view(), name='create-shop'),
                       url(r'^(?P<shop_slug>[\w-]+)/(?P<component_slug>[\w-]+)$', ComponentDetail.as_view(), name="shop-component-detail"),
                       # url(r'^search/?$', ShopSearchView.as_view(), name='shop-search'),
                       # url(r'^shop-autocompete/$', 'app.shop.views.shop_name_autocomplete', name='shop-autocomplete'),
                       )

