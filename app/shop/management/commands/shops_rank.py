from django.core.management.base import BaseCommand
from app.shop.models import Shop

class Command(BaseCommand):
    help = 'calculate shops ranks according to reviews and repaired phones'

    def handle(self, *args, **options):
        shops   =   Shop.objects.filter(blocked=False).order_by('-performance','created')
        rank = 1
        for shop in shops:    
            shop.rank = rank
            rank      += 1
            shop.save()
        self.stdout.write("All shops ranks done")


