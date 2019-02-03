from django.core.management.base import BaseCommand
from app.server.models import Server
from  numpy import transpose, sum
from app.order.models import COMPLETED

LEVELS_COEFFICIENT             =  10000
TURNOVER_COEFFICIENT           =  7 
AVERAGE_REVIEW_COEFFICIENT     =  100
DEPOSIT_COEFFICIENT            =  6
ORDERS_NUMBER_COEFFICIENT      =  5
REVIEWS_COEFFICIENT            =  5
ORDERS_COMPLETED_COEFFICIENT   =  4
RAISED_TICKETS__COEFFICIENT    =  -3
PAID_ORDERS_NUMBER_COEFFICIENT      =  2

COEFFICIENTS = [LEVELS_COEFFICIENT, REVIEWS_COEFFICIENT, TURNOVER_COEFFICIENT, 
    DEPOSIT_COEFFICIENT, ORDERS_NUMBER_COEFFICIENT, ORDERS_COMPLETED_COEFFICIENT,RAISED_TICKETS__COEFFICIENT, PAID_ORDERS_NUMBER_COEFFICIENT ] 

def performance(coefficients, server_array):
    return sum(coefficients*transpose(server_array))

class Command(BaseCommand):
    help = 'calculate servers levels according to reviews and repaired phones'

    def handle(self, *args, **options):
        servers   =   Server.objects.filter(blocked=False)

        for server in servers:
            array = []
            #level
            array.append(int(server.level))
            #reviews
            array.append(server.review_server.all().count())
            #turnover
            total_benefit = float(sum([float(order.amount) for order in server.server_order.filter(paid=True, deleted=False)]))
            array.append(total_benefit)
            #deposit
            array.append(float(server.balance))
            #all orders 
            array.append(server.server_order.all().count())
            #just completed orders
            array.append(server.server_order.filter(status=COMPLETED).count())
            #raised tickets
            raised_tickets = sum([tickets.count() for tickets in [order.order_tickets for order in server.server_order.all()]])
            array.append(raised_tickets)
            #number of phones successfully repaired and paid
            array.append(server.server_order.filter(paid=True, deleted=False).count())
            #the fianl result
            print array
            server.performance = performance(COEFFICIENTS, array)
        
            server.save()
        self.stdout.write("All servers performances done")


        