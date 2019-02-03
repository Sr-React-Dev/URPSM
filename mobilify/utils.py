__author__ = 'Vishwash Gupta'
from django.contrib import admin

ENDPOINT_MONITOR_GROUP = 'Endpoint monitor'
CLIENT_MONITOR_GROUP = 'Client monitor'
SHOP_MONITOR_GROUP = 'Shop monitor'
USER_MONITOR_GROUP = 'User monitor'
SERVER_MONITOR_GROUP = 'Server monitor'
PHONE_MONITOR_GROUP = 'Phone monitor'
COMPONENT_MONITOR_GROUP = 'Component monitor'
ORDER_MONITOR_GROUP = 'Order monitor'
TICKET_MONITOR_GROUP = 'Ticket monitor'
PAYPAL_IPN_MONITOR_GROUP = 'PayPalIpn monitor'
SUBCONTRACTOR_GROUP = 'Subcontractor'


class BaseAdmin(admin.ModelAdmin):
    view_groups = []

    def get_readonly_fields(self, request, obj=None):
        return self.get_read_only_fields_for_permissions(request, self.model, self.readonly_fields)

    def get_read_only_fields_for_permissions(self, request, models, readonly_fields):
        if request.user.groups.filter(name__in=self.view_groups):
            return [f.name for f in models._meta.fields]
        return readonly_fields

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        if request.user.groups.filter(name__in=self.view_groups):
            extra_context['show_save_as_new'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
            extra_context['readonly'] = True

        return super(BaseAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=self.view_groups):
            return False
        else:
            return True

    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=self.view_groups):
            return False
        else:
            return True

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=self.view_groups):
            pass
        else:
            obj.save()


import os, sys, linecache

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    # if 'bootcamp-master' in PROJECT_DIR:
    msg = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print msg
    return msg


