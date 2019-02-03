from django.conf.urls import  patterns, url
from django.conf.urls.i18n import i18n_patterns
from app.launch.views import TestView

urlpatterns = patterns('',
    url(r'^soon/$', 'app.launch.views.signup', name='launch_contact'),
    url(r'^done/$', 'app.launch.views.done', name='done'),
    url(r'^HTTPCS36990.html$', TestView.as_view(), name='test'),
)