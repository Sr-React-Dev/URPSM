from django.core.management.base import BaseCommand
from app.shop.models import Shop
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
CLIENT_NUMBER_COEFFICIENT      =  2

COEFFICIENTS = [LEVELS_COEFFICIENT, REVIEWS_COEFFICIENT, TURNOVER_COEFFICIENT, 
    DEPOSIT_COEFFICIENT, ORDERS_NUMBER_COEFFICIENT, ORDERS_COMPLETED_COEFFICIENT,RAISED_TICKETS__COEFFICIENT, CLIENT_NUMBER_COEFFICIENT ] 

def performance(coefficients, shop_array):
    return sum(coefficients*transpose(shop_array))

class Command(BaseCommand):
    help = 'calculate shops performance according to reviews and repaired phones'

    def handle(self, *args, **options):
        shops   =   Shop.objects.filter(blocked=False)

        for shop in shops:
            array = []
            #level
            array.append(int(shop.level))
            #reviews
            array.append(shop.review_shop.all().count())
            #turnover
            total_benefit = float(sum([client.total_benefit for client in shop.phone_shop.filter(paid=True, deleted=False)]))
            array.append(total_benefit)
            #deposit
            array.append(float(shop.balance))
            #all orders 
            array.append(shop.shop_server_order.all().count())
            #just completed orders
            array.append(shop.shop_server_order.filter(status=COMPLETED).count())
            #raised tickets
            raised_tickets = sum([tickets.count() for tickets in [order.order_tickets for order in shop.shop_server_order.all()]])
            array.append(raised_tickets)
            #number of phones successfully repaired and paid
            array.append(shop.phone_shop.filter(paid=True, deleted=False).count())
            #the fianl result
            print array
            shop.performance = performance(COEFFICIENTS, array)
        
            shop.save()
        self.stdout.write("All shops performances done")


        