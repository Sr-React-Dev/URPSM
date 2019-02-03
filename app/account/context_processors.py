# -*- coding: utf-8 -*-
from random import random
import json
from django.conf import settings
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm


def deposit(request):
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "item_name": "name of the item",
        "invoice": random(),
        "notify_url": ("%s://%s%s") % (request.scheme, request.get_host(), reverse('paypal-ipn')),
        "return_url": "http://www.urpsm.com/",
        "cancel_return": "http://www.urpsm.com/",
        "custom": json.dumps({'shop_uuid': str(request.user.profile.shop.uuid), 'username': request.user.username})

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form_deposit": form}
    return context


def css_direction(request):
    if request.LANGUAGE_CODE == 'ar':
        context = {'PULL_DIRECTION':'pull-left'}
    else:
        context = {'PULL_DIRECTION':'pull-right'}
    return context
