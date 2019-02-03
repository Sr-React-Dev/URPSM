# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from hashlib import sha1
from random import random

from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template
from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def get_key():
    return sha1(str(random()).encode('utf-8')).hexdigest()


def mailer(template_name=None, subject=None, ctx={}, recipient=None,fromemail="confirmations@urpsm.com"):

    ctx['site'] = Site.objects.get_current()
    try:
        message = get_template(template_name).render(Context(ctx))
    except TemplateDoesNotExist:
        raise(_(u'Template Does Not Exist'))

    if recipient is None:
        raise(_(u'Email recipient cannot be null.'))

    if subject is None:
        raise(_(u'Please, Enter a subject.'))
    send_mail(
        subject, message,"contact@urpsm.com",[recipient, ],fail_silently=False,html_message=message)


    
def get_client_ip(request):
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip