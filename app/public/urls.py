from __future__ import absolute_import
from django.conf.urls import patterns, url

from .views import (Home,  TermsView, PrivacyView, ShopPositionView, SearchShopsByCountryAndCity,
                      ModelDetailPage, ShopDetailView, RegistredShopView, RegistredServerView, RepairedPhoneView, LevelPageView,
                       LandingPageView, UnlockedPhoneView, ContactView, ThankyouView, AboutUsView, Error404View, BrandDetailView,
                       PopularPhoneView , PopularShopView  )

urlpatterns = patterns('',
                       url('^$', Home.as_view(), name='home'),
                       url('^terms/$', TermsView.as_view(), name='terms'),
                       url('^privacy/$', PrivacyView.as_view(), name='privacy'),
                       url(r'^markup/$', ShopPositionView.as_view(),name='near-shops'),
                       url(r'^markup/(?P<latLng>[0-9_.-]+)/$', ShopPositionView.as_view(),name='map-data'),
                       # url(r'^search$', SearchShopsByCountryAndCity.as_view(),name='search-shops'),
                       # url(r'^search/$', SearchShopsByCountryAndCity.as_view(),name='search-shops'),
                       url(r'^search/(?P<country>[0-9]+)/(?P<city>[0-9]+)/$', SearchShopsByCountryAndCity.as_view(),name='search-shops'),
                       url(r'^phone$', ModelDetailPage.as_view(), name='phone-info'),
                       url(r'^phone/$', ModelDetailPage.as_view(), name='phone-info'),
                       url(r'^phone/(?P<brand>[\w-]+)/(?P<model>[\w-]+)/$', ModelDetailPage.as_view(),name='model'),
                       url(r'^shop/(?P<shop>[0-9]+)/(?P<slug>[\w-]+)/$', ShopDetailView.as_view(),name='shop-detail-public'),
                       # url(r'^shop/reviews$', 'app.public.views.get_shop_reviews' ,name='shop-reviews'),
                       url(r'^registred-servers$', RegistredServerView.as_view() ,name='registred-servers'),
                       url(r'^registred-shops$', RegistredShopView.as_view() ,name='registred-shops'),
                       url(r'^unlocked-phones$', RegistredShopView.as_view() ,name='registred-phones'),
                       url(r'^unlocked-phones$', UnlockedPhoneView.as_view() ,name='unlocked-phones'),
                       url(r'^repaired-phones$', RepairedPhoneView.as_view() ,name='repaired-phones'),
                       url(r'^popular-phones$', PopularPhoneView.as_view()  ,name='popular-phones'),
                       url(r'^popular-shops$', PopularShopView.as_view()  ,name='popular-shops'),
                       url(r'^contact-us$', ContactView.as_view() ,name='contact-us'),
                       url(r'^about-us$', AboutUsView.as_view() ,name='about-us'),
                       url(r'^thankyou$', ThankyouView.as_view() ,name='thankyou'),
                       url(r'^thankyou$', ThankyouView.as_view() ,name='thankyou'),
                       url(r'^levels$', LevelPageView.as_view() ,name='levels'),
                       url(r'^services$', LandingPageView.as_view() ,name='services'),
                       url(r'^send-feedback$', 'app.public.views.send_feedback', name='send-feedback'),
                       url(r'^brand/(?P<brand>[\w-]+)$', BrandDetailView.as_view(), name='brand'),

                       )
