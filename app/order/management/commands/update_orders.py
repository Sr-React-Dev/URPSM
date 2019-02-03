from django.core.management.base import BaseCommand

from app.account.utils import mailer
from app.order import utils
from app.order.models import *
from django.utils import  timezone
from django.contrib.auth.models import User
from app.notifications.models import Notification
from datetime import datetime, timedelta
from app.order.models import ServerOrder
from app.order.utils import get_order_completion_charges
from app.server.models import ServerSales


class Command(BaseCommand):
    help = 'Update Server Orders'


    def handle(self, *args, **options):
        eligible_server_orders = ServerOrder.objects.filter(status=PENDING)
        for server_order in eligible_server_orders:
            try:
                utils.update_server_order(server_order)
            except:pass
        #delivered orders notifications
        delivered_orders = ServerOrder.objects.filter(status=DELIVERED)
        for order in delivered_orders:
            server = order.server
            shop = order.shop
            if not Notification.objects.filter(notification_type=Notification.ORDER_DELIVERED, server_order=order, server=server, shop=shop).exists():
                users = User.objects.filter(profile__server=server)
                for user in users:
                    user.profile.notify_order_delivered(server, order, shop )
                mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                                     ctx={'notification': 'Order with id #' + str(
                                         order.id) + ' has been delivered.'},
                                     recipient=shop.shop_email,
                                     fromemail="notifications@urpsm.com")
        edge = timezone.now() - timedelta(hours=24)
        completed_orders = ServerOrder.objects.filter(delivery_time__lt=edge,status__in=[COMPLETED,DELIVERED],paid=False)
        for order in completed_orders:
            try:
                o = ServerSales.objects.get(server=order.server,type="amount_completed")
            except ServerSales.DoesNotExist:
                o = ServerSales.objects.create(server=order.server, type="amount_completed",value=Decimal(0.0))
            order.paid = True
            order.save()
            o.value += order.amount - get_order_completion_charges(order.server,order.amount)
            o.save()


        #non delivered orders notifications
        not_delivered_orders = ServerOrder.objects.filter(delivery_time__lt=timezone.now(), status=PENDING)
        for order in not_delivered_orders:
            server = order.server
            shop = order.shop
            if not Notification.objects.filter(
                notification_type=Notification.ORDER_DELIVERY_TIME_EXCEEDED,
                 server_order=order, server=server, shop=shop).exists():
                users = User.objects.filter(profile__server=server)
                for user in users:
                    user.profile.notify_order_delivery_time_exceeded(server, order, shop)
                    mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                       ctx={'notification': 'Order with id #' + str(
                           order.id) + 'is not been delivered on time.'},
                       recipient=shop.shop_email,
                       fromemail="notifications@urpsm.com")
        #close delivery time orders notifications
        edge = timezone.now() + timedelta(hours=1)
        upon_delivery_orders = ServerOrder.objects.filter(delivery_time__lt=edge, status=PENDING)
        for order in upon_delivery_orders:
            server = order.server
            shop = order.shop
            if not Notification.objects.filter(
                notification_type=Notification.ORDER_DELIVERY_TIME_IS_CLOSE,
                 server_order=order, server=server, shop=shop).exists():
                users = User.objects.filter(profile__server=server)
                for user in users:
                    user.profile.notify_order_delivery_time_close(server, order, shop)









