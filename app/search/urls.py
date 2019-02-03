from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^search$', views.search, name='search'),
    # url(r'^shop$', views.shop_search, name='shop-search')
]
