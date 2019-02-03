from __future__ import absolute_import
from django.conf.urls import patterns, url

from .views import create_server_review, create_shop_review, ThankyouView

urlpatterns = patterns(
    '',
    url(r'^thank-you$', ThankyouView.as_view(template_name = "urpsm/ureview/thankyou.html"), name="thank-you"),
    url(r'^thank-you/$', ThankyouView.as_view(template_name='urpsm/v2/client/thankyou_v2.html'), name="thank-client"),
    url(r'^server/(?P<pk>\d+)$',create_server_review, name='review-server'),
    url(r'^shop$',create_shop_review, name='review-shop'),
)
