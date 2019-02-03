from __future__ import absolute_import
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
# from django.http import HttpResponse
from django.http import Http404, JsonResponse
import decimal
from app.payment import utils
from app.payment.models import *
from django.contrib.auth.models import User


@login_required
@csrf_exempt
def transfer_money_from_wallet(request):
    if request.method == 'GET':
        response = {}
        amount_for_transfer = request.GET.get('amount', None)
        if not amount_for_transfer:
            response['message'] = _("Please enter amount to be transferred.")
            response['success'] = False
        else:
            user = request.user
            profile = user.profile
            if not profile:
                response['message'] = "Profile details not found for user"
                response['success'] = False
                return JsonResponse(response)
            server = profile.server
            if not server:
                response['message'] = "Server details not found for user"
                response['success'] = False
                return JsonResponse(response)
            # print 'server balance : ', server.balance
            # print 'amount for transfer : ', amount_for_transfer
            if decimal.Decimal(server.balance) < decimal.Decimal(amount_for_transfer):
                response['message'] = "Amount can not exceed the balance amount."
                response['success'] = False
                return JsonResponse(response)
            payment_transfer_response = utils.transfer_money_to_paypal_account(
                user.email,
                amount_for_transfer)  # replace the hardcoded email with user.email
            if 'success' in payment_transfer_response:
                if payment_transfer_response['success']:
                    server.balance = decimal.Decimal(server.balance) - decimal.Decimal(amount_for_transfer)
                    server.save()
                    users = User.objects.filter(profile__server=server)
                    for user in users:
                        user.profile.notify_accepted_transaction(server)
            else:
                users = User.objects.filter(profile__server=server)
                for user in users:
                    user.profile.notify_declined_transaction(server)

            response = payment_transfer_response
        return JsonResponse(response)
    return Http404


def show_shop_user_payment_transaction(request):
    if request.method == 'POST':
        response = {}
        try:
            try:
                shop = request.user.profile.shop
            except Exception, e:
                # print e
                response['error_message'] = "Shop user Not Found For this User"
                response['error'] = True
                return JsonResponse(response)
            response['shop_payment_transactions'] = ServerPaymentTransaction.objects.filter(shop=shop)
        except Exception, e1:
            # print e1
            response['error_message'] = "Some Error Occurred"
            response['error'] = True
        return JsonResponse(response)
    return Http404


def show_shop_user_payment_transaction(request):
    if request.method == 'POST':
        response = {}
        try:
            try:
                server = request.user.profile.server
            except Exception, e:
                # print e
                response['error_message'] = "Server user Not Found For this User"
                response['error'] = True
                return JsonResponse(response)
            response['server_payment_transactions'] = ShopPaymentTransaction.objects.filter(server=server)
        except Exception, e1:
            # print e1
            response['error_message'] = "Some Error Occurred"
            response['error'] = True
        return JsonResponse(response)
    return Http404