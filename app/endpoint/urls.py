from __future__ import absolute_import
from django.conf.urls import patterns, url
from django.http import HttpResponse

urlpatterns = patterns('',
                       url(r'^get_services/$',
                           'app.endpoint.views.get_services',
                           name="get_services"),
                      
                       url(r'^get_service_detail/$',
                           'app.endpoint.views.get_service_detail',
                           name="get_service_detail"),

                       url(r'^save-selected-services/$',
                           'app.endpoint.views.save_selected_services',
                           name="endpoint-services"),

                       url(r'^set-credit$',
                           'app.endpoint.views.set_credit',
                           name="endpoint-server-credit"),
                       url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\n\nAllow: /",status=200)),

                       )
