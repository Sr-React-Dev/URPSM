from django.core.management.base import BaseCommand
from app.server.models import Server

class Command(BaseCommand):
    help = 'calculate servers performance'

    def handle(self, *args, **options):
        servers   =   Server.objects.filter(blocked=False).order_by('-performance','created')
        rank = 1
        for server in servers:    
            server.rank = rank
            rank      += 1
            server.save()
        self.stdout.write("All servers ranks done")


