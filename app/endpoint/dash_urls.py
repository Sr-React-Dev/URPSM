from django.conf.urls import patterns, url
from .views import EndPointCreateView, EndPointListView, \
                   EndPointOrdersListView, EndPointEditView,\
                   EndPointDispatchView, EndPointNetsAndServicesView, \
                   EndpointDeleteView



urlpatterns = patterns('',
                       url(r'^endpoints/$', EndPointListView.as_view(),
                           name="endpoints-list"),
                       url(r'^endpoints/orders/$', EndPointOrdersListView.as_view(),
                           name="endpoint-orders"),  
                       url(r'^endpoints/dispatch$', EndPointDispatchView.as_view(),
                           name="endpoint-dispatch"),                     
                       url(r'^endpoints/create/$', EndPointCreateView.as_view(),
                           name='endpoint-create'),
                       url(r'^endpoints/create/(?P<extra>\w+)$', EndPointCreateView.as_view(),
                           name='endpoint-create'),
                       url(r'^endpoints/edit/$', EndPointEditView.as_view(),
                           name='endpoint-edit'),
                       url(r'^endpoints/networks-services/$', EndPointNetsAndServicesView.as_view(),
                           name='endpoint-networks'),
                       url(r'^endpoints/networks-deletion/(?P<pk>\d+)$', EndpointDeleteView.as_view(),
                           name='endpoint-delete'),
                       )