from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import  timezone
from app.ureview.models import ServerReview
from app.order.models import ServerOrder, COMPLETED
from app.server.models import Server


class Command(BaseCommand):
    help = 'calculate servers levels according to reviews and repaired phones'

    def handle(self, *args, **options):
        servers   =   Server.objects.filter(blocked=False)

        for server in servers:
            reviews = ServerReview.objects.filter( server=server, rating__gte=3).count()
            unlocked = ServerOrder.objects.filter(server=server ,status=COMPLETED).count()
        	
            if  unlocked < 200 and reviews < 100:
                server.level = "1"
            if  200 <= unlocked < 1000 and 100 <= reviews < 300:
                server.level = "2"
            if   1000 <= unlocked < 5000 and 300 <= reviews < 2000:
                server.level = "3"
            if  5000 <= unlocked < 8000 and 2000 <= reviews < 4000:
                server.level = "4"
            if  unlocked >= 8000 and reviews >=4000:
                server.level = "5"
            
            server.save()
        