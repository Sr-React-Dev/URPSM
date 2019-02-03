from django import template
import ast, json
register = template.Library()
from app.endpoint.models import Endpoint
from django.utils.safestring import mark_safe
from collections import OrderedDict


@register.simple_tag(takes_context=True)
def get_netowrks_and_services(context):
     try:
     	request = context['request']
     	try:
     		endpoint = Endpoint.objects.get(server=request.user.profile.server)
     	except:
     		endpoint = Endpoint.objects.filter(server=request.user.profile.server)[0]
     	networks = endpoint.client.get_imei_service_list(True)
     	_networks = dict()
     	for name, services in networks.iteritems():
            dump = []
            for service in services:
                dump.append(service[0])
        	_networks.update({name:dump})
        _networks = json.dumps(_networks)
     	return mark_safe(_networks)
     except Exception as e:
     	raise e

@register.simple_tag(takes_context=True)
def get_user_netowrks_and_services(context):
    try:
        request = context['request']
        try:
            endpoint = Endpoint.objects.get(server=request.user.profile.server)
        except:
            endpoint = Endpoint.objects.filter(server=request.user.profile.server)[0]
            
        networks = endpoint.networks.all().values('name', 'services')
        _networks  = dict()

        for network in networks:
            services = ast.literal_eval(network['services'])
            dump = []
            for key, value in services.iteritems():
                if not key=='network':
                    dump.append(str(value))
            _networks.update({str(network['name']): dump  })

        return mark_safe(_networks)


    except Exception as e:
        raise e


