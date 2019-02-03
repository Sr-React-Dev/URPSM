from __future__ import absolute_import
from django.contrib.admin.sites import AdminSite

from app.dash.views import view_clearance_requests, edit_site_texts, AdminViewActionHistory, edit_deposit_info, \
    new_message_from_admin, edit_meta


class AdminMixin(object):

    """Mixin for AdminSite to allow custom dashboard views."""

    def __init__(self, *args, **kwargs):
        return super(AdminMixin, self).__init__(*args, **kwargs)

    def get_urls(self):
        """Add our dashboard view to the admin urlconf. Deleted the default index."""
        from django.conf.urls import patterns, url
        from .views import Dashboard,AdminSupportTicket,view_shop_invoices,verify_shop_proof,urpsm_charges

        urls = super(AdminMixin, self).get_urls()
        del urls[0]
        custom_url = patterns('',
                              url(r'^$', self.admin_view(Dashboard.as_view()),
                                  name="index"),
                              url(r'^urpms-charges$',urpsm_charges,name="urpsm-custom-charges"),
                              url(r'^ticket/orderticket/(?P<pk>\d+)/',AdminSupportTicket),
                              url(r'^clearance-requests',view_clearance_requests,name="view-clearance-requests"),
                              url(r'^view-shop-invoices$',view_shop_invoices,name="view-shop-invoices"),
                              url(r'^admin-proof-verify/(?P<pk>\d+)/$',verify_shop_proof,name="admin-proof-verify"),
                              url(r'^edit-site$',edit_site_texts,name='edit_site_texts'),
                              url(r'^adminmessages/$', new_message_from_admin, name='contact-shop-server'),
                              url(r'^edit-deposit-info',edit_deposit_info,name='edit_deposit_info'),
                              url(r'^actionhistory',AdminViewActionHistory,name="actionhistoryadmin"),
                              url(r'^edit-meta-tags$',edit_meta,name="edit-meta")
                              )

        return custom_url + urls


class SitePlus(AdminMixin,  AdminSite):

    """
    A Django AdminSite with the AdminMixin to allow registering custom
    dashboard view.
    """
