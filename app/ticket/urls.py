from __future__ import absolute_import
from django.conf.urls import patterns, url

from .views import TicketDetailView, create_message

urlpatterns = patterns(
    '',
    url(r'^(?P<ticket_id>\d+)/create_message/$', create_message, name="create_message"),
    url(r'^(?P<pk>\d+)/detail/$',TicketDetailView.as_view(), name='ticket_detail'),
)
