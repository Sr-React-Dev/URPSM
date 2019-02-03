from django.contrib import admin
from .models import Notification
from app.shop.models import Shop
from app.server.models import Server

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user','message')
    def get_queryset(self, request):
        print request.GET
        shop =request.GET.get('shop', None)
        server =request.GET.get('server', None)
        qs = super(NotificationAdmin, self).get_queryset(request)
        if shop:
            shop = Shop.objects.get(pk=int(shop))
            return qs.filter(shop=shop, notification_type__in=['A','B'])
        elif server:
            server = Server.objects.get(pk=int(server))
            return qs.filter(server=server, notification_type__in=['A','B'])
        else:
            return qs
    

# class ShopNotificationAdmin(admin.ModelAdmin):
#     list_display = ('shop', 'from_user', 'to_user', 'message')

# class ServerNotificationAdmin(admin.ModelAdmin):
#     list_display = ('server', 'from_user', 'to_user', 'message')


admin.site.register(Notification, NotificationAdmin)
# admin.site.register(Notification, ShopNotificationAdmin)
# admin.site.register(Notification, ServerNotificationAdmin)