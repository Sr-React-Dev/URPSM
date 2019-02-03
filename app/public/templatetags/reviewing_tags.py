import base64
import json

import re
from django import template
from django.utils.safestring import mark_safe

from app.dash.models import KeyValueStore

register = template.Library()
from django.utils.translation import ugettext_lazy as _
STATUS_CHOICES = {
        'p': unicode(_("Pending")),
        'c': unicode(_("Need Your Call")),
        'r': unicode(_("Ready")),
        'n': unicode(_("Can't Repaired")),
    }

@register.filter
def div( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value / arg
    except: pass
    return ''

@register.filter
def multiply( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = float( value )
        arg = float( arg )
        if arg: return value * arg
    except: pass
    return ''

@register.filter
def subtract(value, arg):
    if value > arg:
        return value - arg
    else:
        return 0
@register.filter(name='times') 
def times(number):
    return range(number)


@register.filter
def status_name(value):
    return STATUS_CHOICES.get(value, unicode( _('Undefined') ) )

@register.filter
def url_to_meta(url):
    try:
        url = re.sub('/en/','/',url.rstrip())
        url = re.sub('/fr/', '/', url.rstrip())
        url = re.sub('/ar/', '/', url.rstrip())
        metatags = KeyValueStore.objects.get(key=url).value
        metatagsjson = base64.b64decode(metatags)
        obj = json.loads(metatagsjson)['tags']
        html = ""
        for i in obj:
            html += "<meta title='"+i['name']+"' content='"+i['content']+"'>"
        html = mark_safe(html)
        return html
    except:
        return ""