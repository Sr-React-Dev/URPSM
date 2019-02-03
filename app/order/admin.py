# -*- coding: utf-8 -*-

import decimal
import json
from django.contrib import admin

from app.dash.models import AdminActionHistory
from .models import ServerOrder
from mobilify import utils


def refund_action(modeladmin, request, queryset):
    for order in queryset:
        amount = decimal.Decimal(order.amount)
        order.shop.balance += amount
        order.shop.save()
        order.amount = 0
        order.save()


refund_action.short_description = u'Refund the order'


class ServerOrderAdmin(utils.BaseAdmin):
    view_groups = [utils.ORDER_MONITOR_GROUP]
    list_display = ('ref', 'imei', 'get_shop_buyer', 'get_shop_seller',
                    'endpoint',
                    'get_service', 'amount', 'paid')
    list_filter = ['server', 'endpoint', 'shop', 'paid']
    search_fields = ['server','endpoint', 'shop', 'service', 'imei']
    list_editable = ['paid']
    actions = [refund_action, ]

    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "Order "+t+" #"+str(obj.id)
        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(ServerOrderAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def get_shop_buyer(self, obj):
        return obj.shop

    get_shop_buyer.short_description = u'Shop (Buyer)'

    def get_shop_seller(self, obj):
        return obj.endpoint.server

    get_shop_seller.short_description = u'Shop (Seller)'

    def get_service(self, obj):
        return obj.get_service

    get_service.short_description = u'Service'


admin.site.register(ServerOrder, ServerOrderAdmin)
