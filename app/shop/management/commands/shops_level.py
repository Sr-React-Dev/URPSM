from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import  timezone
from app.ureview.models import ShopReview
from app.client.models import Client
from app.shop.models import Shop


class Command(BaseCommand):
    help = 'calculate shops levels according to reviews and repaired phones'

    def handle(self, *args, **options):
        shops   =   Shop.objects.filter(blocked=False)

        for shop in shops:
            reviews = ShopReview.objects.filter( shop=shop, rating__gte=3).count()
            repaired = Client.objects.filter(shop=shop, todo="r" ,status='r').count()
            unlocked = Client.objects.filter(shop=shop, todo="u" ,status='r').count()
        	
            if repaired < 200 and unlocked < 200 and reviews < 100:
                shop.level = "1"
            if  200 <= repaired < 1000 and 200 <= unlocked < 1000 and 100 <= reviews < 300:
                shop.level = "2"
            if 1000 <= repaired < 5000 and  1000 <= unlocked < 5000 and 300 <= reviews < 2000:
                shop.level = "3"
            if 5000 <= repaired < 8000 and 5000 <= unlocked < 8000 and 2000 <= reviews < 4000:
                shop.level = "4"
            if repaired >= 8000 and unlocked >= 8000 and reviews >=4000:
                shop.level = "5"
            
            shop.save()
        