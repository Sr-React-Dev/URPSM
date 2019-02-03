# Created by Vishwash Gupta

import datetime
import decimal

from django.utils import timezone
from django.db import transaction

from app.dhrufusion.client import Client as DhruClient
from app.order.models import *
from app.payment.models import CREDIT
from app.payment import utils as payment_utils
from app.account import utils as account_utils
import app.ticket.utils as ticket_utils

import json
import re

ORDER_CANCELLATION_CHARGE_FACTOR = 2
ORDER_COMPLETION_CHARGE_FACTOR = 5

def get_order_cancellation_charges(shop,amount):
    if shop.cancellation_charges is None:
        charges = Charges.objects.get(charge='order_cancellation_charges').value
    else:
        charges = shop.cancellation_charges
    if '%' in charges:
        return amount*decimal.Decimal(charges[:-1])/100
    else:
        return decimal.Decimal(charges)

def get_order_completion_charges(server,amount):
    if server.completion_charges is None:
        charges = Charges.objects.get(charge='order_completion_charges').value
    else:
        charges = server.completion_charges
    if '%' in charges:
        return amount*decimal.Decimal(charges[:-1])/100
    else:
        return decimal.Decimal(charges)





def cancel(order):
    return __cancel_server_order(order)

def complete(order):
    return  __complete_server_order(order)

def validate_server_order_for_cancellation(server_order):
    print "delivery time: ", server_order.delivery_time
    print "current time: ", timezone.now()
    print "status: ", server_order.status
    if server_order.status == PENDING:
        if server_order.delivery_time >= timezone.now():
            print "order delivery time hasn't been passed yet"
            return False
        else:
            print "order delivery time has passed, thus can be cancelled"
            return True
    elif server_order.status == DELIVERED:
        if server_order.delivery_time + datetime.timedelta(hours=24) > timezone.now():
            print "order within 24 hrs delivery time"
            return True
        else:
            print "order past 24 hrs delivery time already"
            return False
    elif server_order.status == REJECTED:
        print "order is already rejected"
        return False
    else:
        return False


@transaction.atomic()
def __complete_server_order(server_order):
    if server_order.status == COMPLETED:
        return server_order
    server_order.status = COMPLETED
    order_amount = decimal.Decimal(server_order.amount)
    charges = get_order_completion_charges(server_order.server,order_amount)
    charges = round(charges, 2)
    print "order_amount : ", order_amount
    print "charges : ", charges
    order_amount = round(order_amount, 2)
    server_wallet_amount = order_amount - charges
    print "server_wallet_amount: ", server_wallet_amount
    server_order.server.credit += decimal.Decimal(server_wallet_amount)
    server_order.urpsm_charge = charges
    server_order.urpsm_charge_factor = ORDER_COMPLETION_CHARGE_FACTOR
    server_order.server.save()
    payment_utils.create_server_payment_transaction(server_order.server, server_wallet_amount,
                                                    server_order.server.credit, CREDIT,
                                                    "Amount credit for order ID: " + str(server_order.id))
    server_order.save()
    return server_order



@transaction.atomic()
def update_server_order(server_order):
    if server_order.endpoint.provider == 'dhru':
        status = get_order_status_from_dhru(server_order)
    elif server_order.endpoint.provider == 'naksh' or server_order.endpoint.provider == 'gsm':
        c = server_order.endpoint.client
        if c.status():
            od = json.loads(c.get_imei_order(id=server_order.ref))
            if od['status'] == 'completed':
                status = '4'
            elif od['status'] == 'rejected':
                status = '3'
            elif od['status'] == 'in process' or od['status'] == 'pending':
                status = '0'
    if not status:
        return None
    if status == '0':
        server_order.status = PENDING
    elif status == '3' and server_order.status != REJECTED:
        server_order.status = REJECTED
        order_amount = decimal.Decimal(server_order.amount)
        charges = 0.00
        print "order_amount : ", order_amount
        print "charges : ", charges
        order_amount = round(order_amount, 2)
        refund_amount = order_amount
        print "refund_amount: ", refund_amount
        server_order.shop.balance += decimal.Decimal(refund_amount)
        server_order.urpsm_charge = charges
        server_order.urpsm_charge_factor = 0
        server_order.shop.save()
        payment_utils.create_shop_payment_transaction(server_order.shop, refund_amount, server_order.shop.balance,
                                                      CREDIT, "(Order Rejected) Amount credit for order ID: " + str(server_order.id))
    elif status == '4':
        server_order.status = DELIVERED
        if server_order.delivery_time + datetime.timedelta(hours=24) <= timezone.now():
            server_order = __complete_server_order(server_order)
    server_order.save()
    return server_order


def complete_hold_server_order(server_order):
    if server_order.status == HOLD:
        server_order = __complete_server_order(server_order)
        return server_order
    else:
        return None


@transaction.atomic()
def __cancel_server_order(server_order):
    if server_order.status == CANCELLED:
        return server_order
    server_order.status = CANCELLED
    print "order is valid for cancellation"
    order_amount = decimal.Decimal(server_order.amount)
    charges = get_order_cancellation_charges(server_order.shop,order_amount)
    charges = round(charges, 2)
    print "order_amount : ", order_amount
    print "charges : ", charges
    order_amount = round(order_amount, 2)
    refund_amount = order_amount - charges
    print "refund_amount: ", refund_amount
    server_order.shop.balance += decimal.Decimal(refund_amount)
    server_order.urpsm_charge = charges
    server_order.urpsm_charge_factor = ORDER_CANCELLATION_CHARGE_FACTOR
    server_order.shop.save()
    server_order.save()
    payment_utils.create_shop_payment_transaction(server_order.shop, refund_amount, server_order.shop.balance,
                                                  CREDIT, "(Order Cancelled) Amount credit for order ID: " + str(server_order.id))
    server_order_profile = server_order.server.user_server.filter()[0]
    shop_order_profile = server_order.shop.user_shop.filter()[0]
    # Notification.objects.create(from_user=shop_order_profile.user,
    #                             to_user=server_order_profile.user, server=server_order.server,
    #                             shop=server_order.shop, server_order=server_order,
    #                             notification_type=Notification.ORDER_CANCELED)
    shop_users = User.objects.filter(profile__shop=server_order.shop)
    for user in shop_users:
        user.profile.notifiy_order_cancelled(server_order.server, server_order.shop, server_order)
    server_users = User.objects.filter(profile__server=server_order.server)
    for user in server_users:
        user.profile.notifiy_order_cancelled(server_order.server, server_order.shop, server_order)
    
    account_utils.mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                                       ctx={'notification':'Order with id #'+str(server_order.id)+' has been cancelled.'}, recipient=server_order.server.server_email,
                                       fromemail="notifications@urpsm.com")
    account_utils.mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                         ctx={'notification': 'Order with id #' + str(server_order.id) + ' has been cancelled.'},
                         recipient=server_order.shop.shop_email,
                         fromemail="notifications@urpsm.com")
    return server_order


def cancel_hold_server_order(server_order):
    if server_order.status == HOLD:
        server_order = __cancel_server_order(server_order)
        return server_order
    else:
        return None


@transaction.atomic()
def validate_and_cancel_server_order(server_order, shop_comments, shop_files):
    server_order = update_server_order(server_order)
    if validate_server_order_for_cancellation(server_order):
        #Refresh order status
        server_order = update_server_order(server_order)
        if server_order.status == REJECTED or server_order.status == PENDING:
            server_order = __cancel_server_order(server_order)
            return [True, None]
        elif server_order.status == DELIVERED:
            server_order.status = HOLD
            print "order is valid for cancellation, thus changing status to hold"
            server_order.save()
            ticket = ticket_utils.create_ticket_for_order(server_order, shop_comments, shop_files)
            users = User.objects.filter(profile__server=server_order.server)
            for user in users:
                account_utils.mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                                 ctx={
                                     'notification': 'You have got a new ticket with id #' + str(ticket.id) + ' for order id #'+str(server_order.id)},
                                 recipient=user.email,
                                 fromemail="notifications@urpsm.com")
            return [True, ticket]
        else:
            return [False,None]

    else:
        print "order is NOT valid for cancellation"
        return [False, None]


def get_order_status_from_dhru(server_order):
    print 'username: ', server_order.endpoint.username
    print 'dhrufusion_url: ', server_order.endpoint.url
    print 'apiaccesskey: ', server_order.endpoint.key
    c = DhruClient(dhrufusion_url=server_order.endpoint.url,
                   username=server_order.endpoint.username,
                   apiaccesskey=server_order.endpoint.key)
    if c.status():
        order_details = json.loads(c.get_imei_order(id=server_order.ref))
        print 'order_details from dhru api: ', order_details
        status = order_details.get('status')
        return status
    else:
        return None

def get_naksh_delivery_date(datestr):
    day_match_reg = '(\d+)[\W]{0,2}[a-z]*[\W]{0,2}d'
    hour_match_reg = '(\d+)[\W]{0,3}h'
    minute_match_reg = '(\d+)[\W]{0,3}m'
    d_m_obj = re.search(day_match_reg,datestr, re.I | re.M)
    h_m_obj = re.search(hour_match_reg,datestr,re.I|re.M)
    m_m_obj = re.search(minute_match_reg,datestr,re.I|re.M)
    if d_m_obj:
        return datetime.datetime.now()+datetime.timedelta(days=int(d_m_obj.group(1)))
    elif h_m_obj:
        return datetime.datetime.now()+datetime.timedelta(hours=int(h_m_obj.group(1)))
    elif m_m_obj:
        return datetime.datetime.now()+datetime.timedelta(minutes=int(m_m_obj.group(1)))
    else:
        return datetime.datetime.now()+datetime.timedelta(days=1)





