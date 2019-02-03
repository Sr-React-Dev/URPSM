from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from app.notifications.models import Notification
from app.order.utils import cancel
from app.ticket.models import *
from django.utils import  timezone
import datetime

from django.db import transaction
User = get_user_model()
class Command(BaseCommand):
    help = 'Update Pending Tickets'

    @transaction.atomic
    def handle(self, *args, **options):
        help = 'Update Pending Tickets and notifiy their respective users'
        eligible_tickets = OrderTicket.objects.filter(last_updated_at__lt=timezone.now() - datetime.timedelta(hours=72), status=INITIATED)
        counter = 0
        for eligible_ticket in eligible_tickets:
            if eligible_ticket.server_comments is not None and eligible_ticket.shop_comments is not None:
                eligible_ticket.status = ADMIN_SUPPORT
                eligible_ticket.save()
            elif eligible_ticket.server_comments is None:
                cancel(eligible_ticket.server_order)
            #notify ticket shop owner & server owner
            if not Notification.objects.filter(notification_type__in=[Notification.NO_SERVER_RESPONSE_SERVER,Notification.NO_SERVER_RESPONSE_SHOP], ticket=eligible_ticket,
                server_order=eligible_ticket.server_order, server=eligible_ticket.server_order.server, shop=eligible_ticket.server_order.shop).exists():
                    server_users = User.objects.filter(profile__server=eligible_ticket.server_order.server)
                    shop_users = User.objects.filter(profile__shop=eligible_ticket.server_order.shop)
                    for user in server_users:
                        user.profile.notify_no_server_response_server(eligible_ticket.server_order, eligible_ticket.server_order.server, eligible_ticket )
                    for user in shop_users:
                        user.profile.notify_no_server_response_shop(eligible_ticket.server_order, eligible_ticket.server_order.shop, eligible_ticket )
            counter +=1
        msg = "%s tickets processed" % counter
        self.stdout.write(msg)








