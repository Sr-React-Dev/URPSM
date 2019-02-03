from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse

from app.dash.sites import SitePlus
from django.conf.urls.i18n import i18n_patterns
from app.account.views import Error404View

admin.site = SitePlus()
admin.autodiscover()

urlpatterns = i18n_patterns('',
                       # Examples:
                       # url(r'^$', 'mobilify.views.home', name='home'),
                       url(r'', include('app.public.urls')),
                       url(r'^orders/', include('app.order.urls')),
                       url(r'^accounts/', include('app.account.urls')),
                       url(r'^shop/', include('app.shop.urls')),
                       url(r'^clients/', include('app.client.urls')),
                       url(r'^components/', include('app.component.urls')),
                       url(r'^server/', include('app.server.urls')),
                       url(r'^select2/', include('django_select2.urls')),
                       url(r'^chaining/', include('smart_selects.urls')),
                       url(r'^notifications/', include('app.notifications.urls')),
                       url(r'^payments/', include('app.payment.urls')),
                       url(r'^tickets/', include('app.ticket.urls')),
                       url(r'^reviews/', include('app.ureview.urls')),
                       url(r'^manager/', include('app.dash.urls')),
                       url(r'^endpoint/', include('app.endpoint.dash_urls')),
                       url(r'^location_field/',
                           include('location_field.urls')),
                       url(r'^payment/',
                           include('paypal.standard.ipn.urls')),
                       url(r'^error', Error404View.as_view(), name='error-404'),
                       url(r'secure/', include('two_factor.urls', 'two_factor')),
                       url(r'sitemap.xml',lambda r: HttpResponse(open('sitemap.xml','r').read(),status=200)))

urlpatterns +=    patterns('',url(r'^urpsmadminp/', include(admin.site.urls)),
                       url(r'^', include('app.endpoint.urls')),
                       url(r'^', include('app.launch.urls')),
                       url(r'', include('social.apps.django_app.urls', namespace='social')),
                       url(r'^search/', include('app.search.urls')),
                       url(r'session_security/', include('session_security.urls')),
                    )

if settings.DEBUG:
    urlpatterns +=patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
                            )

    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            )
