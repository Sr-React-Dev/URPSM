from django import template
import json
register = template.Library()
from simplecities.models import City, Country
from django.utils.safestring import mark_safe
from collections import OrderedDict

def gen(v): yield v

@register.simple_tag(takes_context=True)
def get_countries(context):
    to_return = OrderedDict(Country.objects.all().order_by('name').values_list('name','id'))
    return mark_safe(json.dumps(to_return))

@register.simple_tag(takes_context=True)
def get_cities_countries(context):
    to_return = OrderedDict(City.objects.all().order_by('name',  'country__name').values_list('name', 'country__id'))
    return mark_safe(json.dumps(to_return))
@register.simple_tag(takes_context=True)
def get_cities_ids(context):
    to_return = OrderedDict(City.objects.all().order_by('name', 'country__name').values_list('name', 'id'))
    return mark_safe(json.dumps(to_return))


