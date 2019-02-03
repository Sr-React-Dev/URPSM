from django.contrib import admin

from app.dash.models import AdminActionHistory
from .models import OrderTicket, TicketMessage
from mobilify import utils

# Register your models here.


class OrderTicketAdmin(utils.BaseAdmin):
    change_list_template = 'admin/ticket/orderticket/change_list.html'

    view_groups = [utils.TICKET_MONITOR_GROUP]
    list_display = ('id', 'server_order', 'created_at', 'status', 'shop_response', 'server_response')
    list_display_links = ('id', 'server_order')
    list_filter = ['id', 'server_order', 'status', 'server_order__imei', 'server_order__id']
    search_fields = ['status' 'server_order']

    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "Ticket "+t+" #"+str(obj.id)
        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(OrderTicketAdmin, self).save_model(request, obj, form, change)

admin.site.register(OrderTicket, OrderTicketAdmin)
admin.site.register(TicketMessage)
