import urllib2
from django.utils import timezone

from app.order.models import *
from app.payment.models import ServerPaymentTransaction, ShopPaymentTransaction
from mobilify import settings as mobilify_settings


def transfer_money_to_paypal_account(paypal_email, amount):
    response = {}
    data = json.dumps({
        "actionType": "PAY",
        "receiverList": {
            "receiver":
                [{"amount": str(amount),  # "1.00"
                  "email": paypal_email  # ""ankittaxiforsurechoudhary-buyer@gmail.com""
                  }]
        },
        "currencyCode": "USD",
        "cancelUrl": mobilify_settings.PAYPAL_CANCEL_URL,
        "returnUrl": mobilify_settings.PAYPAL_RETURN_URL,
        "requestEnvelope": {
            "errorLanguage": "en_US",
            "detailLevel": "ReturnAll"
        },
        "senderEmail": mobilify_settings.PAYPAL_SENDER_EMAIL
    })

    request = urllib2.Request(mobilify_settings.PAYPAL_ADAPTIVE_PAYMENT_URL, data,
                              headers=mobilify_settings.request_headers)
    contents = urllib2.urlopen(request)
    json_data = json.load(contents)
    print "response from API: ", json_data
    try:
        payment_status = str(json_data['paymentExecStatus'])
        print "payment_status: ", payment_status
        if payment_status == 'ERROR':
            error_message = str(json_data['payErrorList']['payError'][0]['error']['message'])
            response['success'] = False
            response['message'] = error_message
        elif payment_status == 'COMPLETED':
            response['success'] = True
            payment_info_list = json_data.get('paymentInfoList')
            print payment_info_list
            if payment_info_list is None:
                response['message'] = "Payment is Complete with paypal transcationId:"+payment_info_list['paymentInfo'][0]['transactionId']
            else:
                email = str(payment_info_list['paymentInfo'][0]['receiver']['email'])
                response['message'] = "Payment is Complete, Payment is sent to " + email
    except Exception, e:
        print e
        response['success'] = False
        response['message'] = "Some Error Occurred! Please Try Again", Exception
    print "response: ", response
    return response


def create_server_payment_transaction(server, amount, balance, payment_type, description):
    server_payment_transaction = ServerPaymentTransaction(server=server, amount=amount, balance=balance,
                                                          payment_type=payment_type, description=description,
                                                          created_at=timezone.now())
    server_payment_transaction.save()


def create_shop_payment_transaction(shop, amount, balance, payment_type, description):
    shop_payment_transaction = ShopPaymentTransaction(shop=shop, amount=amount, balance=balance,
                                                      payment_type=payment_type, description=description,
                                                      created_at=timezone.now())
    shop_payment_transaction.save()
