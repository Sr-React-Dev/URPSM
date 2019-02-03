from django.core.management.base import BaseCommand
from app.order import utils
from app.order.models import ShopOrder, ServerOrder, DELIVERED, COMPLETED, CANCELLED, READY
from app.ureview.models import ReviewedOrder
from app.account.models import Profile
from app.notifications.models import Notification
from datetime import timedelta
from django.utils import  timezone


class Command(BaseCommand):
    help = 'Get good orders for reviewing'

    def handle(self, *args, **options):
        shop_orders   =   ShopOrder.objects.filter(delivery_time__gt=timezone.now()+timedelta(days=1), status=READY)

        for order in shop_orders:
        	if not ReviewedOrder.objects.filter(order=order, user=order.client).exists():
        		user_profile = Profile.objects.get(shop=order.shop)
        		user_profile.has_to_review = True
        		user_profile.save()
        		Notification.objects.create(from_user=order.shop.user_shop.all()[0].user,
                                to_user=order.shop.client, 
                                shop=order.shop, shop_order=order,
                                notification_type=Notification.SHOP_REVIEW)
        
        server_orders = ServerOrder.objects.filter(delivery_time__gt=timezone.now()+timedelta(days=1), status=[CANCELLED, COMPLETED])

        for order in server_orders:
        	if not ReviewedOrder.objects.filter(order=order, user=order.client).exists():
        		user_profile = Profile.objects.get(shop=order.shop)
        		user_profile.has_to_review = True
        		user_profile.save()
        		Notification.objects.create(from_user=order.server.user_server.all()[0].user,
                                to_user=order.shop.user_shop.all()[0].user, 
                                shop=order.shop, server_order=order, server=order.server,
                                notification_type=Notification.SERVER_REVIEW)