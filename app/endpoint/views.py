from __future__ import absolute_import
import ast, json
import re

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, ListView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from .forms import EndPointForm, EndPointNetworkForm
from app.dhrufusion.client import Client
from .models import Endpoint, Network
from app.order.models import ServerOrder, Charges
from app.account.views import HasBusinessMixin
from decimal import Decimal

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class EndpointDeleteView(LoginRequiredMixin,GroupRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'urpsm/endpoint/endpoint_confirm_delete.html'
    model = Endpoint
    group_required = u'Administrator'
    success_url = reverse_lazy('endpoints-list')
    success_message = _("The API has been deleted.")

class EndPointOrdersListView(LoginRequiredMixin,GroupRequiredMixin, ListView):
    template_name = 'urpsm/endpoint/orders.html'
    model = ServerOrder
    context_object_name = 'orders'
    paginated_by = 15
    group_required = u'Administrator'

    def get_queryset(self):
        return ServerOrder.objects.select_related().filter(endpoint__server=self.request.user.profile.server)

class EndPointListView(LoginRequiredMixin,GroupRequiredMixin, ListView):
    template_name = 'urpsm/endpoint/list.html'
    model = Endpoint
    context_object_name = 'endpoints'
    paginated_by = 15
    group_required = u'Administrator'

    def get_queryset(self):
        return Endpoint.objects.select_related().filter(server=self.request.user.profile.server)



class EndPointEditView(LoginRequiredMixin,GroupRequiredMixin,
                         SuccessMessageMixin, UpdateView):
    model = Endpoint
    template_name = 'urpsm/endpoint/create.html'
    form_class = EndPointForm
    success_message = _("Your API is successfully updated.")
    group_required = u'Administrator'

    def get_form_kwargs(self):
        kwargs = super(UpdateView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_object(self, queryset=None):
        try:
            return Endpoint.objects.get(server = self.request.user.profile.server)
        except:
            return Endpoint.objects.filter(server = self.request.user.profile.server)[0]

class EndPointNetsAndServicesView(LoginRequiredMixin, GroupRequiredMixin,
                                  AjaxableResponseMixin, UpdateView):
    model           = Endpoint
    template_name   = 'urpsm/endpoint/networks.html'
    form_class      = EndPointNetworkForm
    success_message = _("Your networks and services are successfully updated.")
    group_required  = u'Administrator'


    def get_form_kwargs(self):
        kwargs = super(UpdateView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_object(self, queryset=None):
        try:
            return Endpoint.objects.get(server = self.request.user.profile.server)
        except:
            return Endpoint.objects.filter(server = self.request.user.profile.server)[0]
    
    
class EndPointDispatchView(LoginRequiredMixin,GroupRequiredMixin, View):
    group_required = u'Administrator'
    
    def get(self, request):
        if Endpoint.objects.filter(server= self.request.user.profile.server).exists():
           return redirect('endpoint-edit')
        else:
           return redirect('endpoint-create')


class EndPointCreateView(LoginRequiredMixin,GroupRequiredMixin,
                         SuccessMessageMixin, CreateView):
    template_name   = 'urpsm/endpoint/create.html'
    form_class      = EndPointForm
    success_message = _("Your API was sent successfully.")
    group_required  = u'Administrator'

    def get_success_url(self):
        last_endpoint = Endpoint.objects.filter(server=self.request.user.profile.server).latest('id')
        if last_endpoint.provider == 'naksh' or last_endpoint.provider == 'gsm':
            return reverse_lazy('endpoint-create', kwargs={'extra': 'credit'}, current_app='app.endpoint')
            
        return reverse_lazy('endpoint-create')

    def form_valid(self, form):
        endpoint = form.save(commit=False)
        endpoint.server = self.request.user.profile.server
        endpoint.save()
        return super(EndPointCreateView, self).form_valid(form)


@login_required
@csrf_exempt
def set_credit(request):
    credit = request.POST.get('credit', None)
    
    if credit:
        credit = Decimal(credit)
        if credit > 0:
            request.user.profile.server.credit += Decimal(credit)
            request.user.profile.server.save()
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False, 'error':_('credit must be positive')})
            
    else:
        return JsonResponse({'status':False, 'error':_('No credit provided')})


@login_required
@csrf_exempt
def _get_services(request):
    if(request.method == 'POST' and
            request.POST.get('network', None) is not None):
        c = Client(dhrufusion_url=request.POST.get('url').strip(),
                   username=request.POST.get(
            'username').strip(), apiaccesskey=request.POST.get('key').strip())
        result = c.get_services_list(
            network=request.POST.get('network').strip())
        return JsonResponse(json.loads(result))

    if(request.method == 'POST' and
            request.POST.get('endpoint', None) is not None):
        endpoint = Endpoint.objects.get(
            pk=int(request.POST.get('endpoint').strip()))
        services = endpoint.service
        return JsonResponse({"services": services})

    return JsonResponse({"services": ""})

@login_required
@csrf_exempt
def get_services(request):

    if(request.method == 'POST' and
            request.POST.get('network', None) is not None):
        endpoint_id = request.POST.get('endpoint')
        endpoint = Endpoint.objects.get(pk=int(endpoint_id))
        id = request.POST.get('network').strip()
        network = endpoint.networks.get(pk=id)
        services = network.services
        services = re.sub("'","\"",services)
        services = re.sub("u\"","\"",services)
        return JsonResponse({"services": services})

    return JsonResponse({"services": ""})


@login_required
@csrf_exempt
def get_service_detail(request):
    if (request.method == 'POST' and
            request.POST.get('service', None) is not None and
            request.POST.get('endpoint', None) is not None):

        endpoint = Endpoint.objects.get(pk=int(request.POST.get('endpoint')))
        service = request.POST.get('service')
        c = endpoint.client
        result = c.get_imei_service_detail_new(id=service)
        if request.user.profile.shop:
            shop = request.user.profile.shop
            if shop.completion_charges == None:
                urpsm_charge = Charges.objects.get(charge='order_shop_completion_charges').value
            else:
                urpsm_charge = shop.completion_charges
            if '%' in urpsm_charge:
                urpsm_charge_amount = Decimal(result['credit']) * Decimal(urpsm_charge[:-1]) / 100
            else:
                urpsm_charge_amount = Decimal(urpsm_charge)
            result['credit'] = str(Decimal(result['credit']) + urpsm_charge_amount)

        return JsonResponse(result)
    return JsonResponse({})

def get_clean_data_dict(data):
    clean_data = {}
    for rank,item  in data.iteritems():
        network = endpoint = service_title = id=  None
        service_data   = {}
        if 'network' in item:
            network    = item['network']
        if 'service' in item:
            service_title =    item['service']
        if 'id' in item:
            id =    item['id']
        if not network in clean_data:
            clean_data.update({network:{id:service_title, 'network':network}})
        else:
            clean_data[network].update({id:service_title, 'network':network})

    return clean_data


def add_new_network(new_network_name, network_services_data, endpoint):
    try:
        new_services = json.dumps(network_services_data)
        new_network  = Network.objects.create(services=new_services, name=new_network_name)
        endpoint.networks.add(new_network)

        return _('%s network is successfully added' % new_network_name), None
    except:
        return None, _('error adding network %s' % new_network_name)


def edit_network_services(network_name, network_services_data, endpoint):
    try:
        edited_network    = endpoint.networks.get(name=network_name)
        existing_services = ast.literal_eval(edited_network.services) 
        if not existing_services == network_services_data:
            edited_network.services = network_services_data
            edited_network.save()
        else:
            pass

        return _('%s network is successfully edited' % network_name), None
    except Exception as e:
        raise 
        return None, _('error editing network %s' % network_name)
from mobilify.utils import PrintException
def remove_existing_network(existent_network, endpoint):
    try:
        network = endpoint.networks.get(name=existent_network)
        endpoint.networks.remove(network)
        network.delete()

        return _('%s network is successfully removed' % existent_network), None
    except:
        PrintException()
        return None, _('error removing network %s' % existent_network)

@login_required
@csrf_exempt
def save_selected_services(request):
    try:
        e = Endpoint.objects.get(server=request.user.profile.server)
    except Exception as e:
        return JsonResponse({'status':False, 'errors':str(e)})
    errors =  []
    messages =  []
    data = json.loads(request.POST['data'])

    clean_data = get_clean_data_dict(data)

    existing_networks = e.networks.all()
    existing_networks_names = [ net.values()[0] for  net in existing_networks.values('name')  ]

    new_networks_names = clean_data.keys()


    for new_network_name in new_networks_names:
        if not new_network_name in existing_networks_names:
            network_services_data = clean_data[new_network_name]
            message, error = add_new_network(new_network_name, network_services_data, e)
            if message: messages.append(message)
            if error: errors.append(error)
        else:
            new_services = clean_data[new_network_name]
            message, error = edit_network_services(new_network_name, new_services, e)
            if message: messages.append(message)
            if error: errors.append(error)
    for existent_network_name in existing_networks_names:
        if not existent_network_name in new_networks_names:
            message, error = remove_existing_network(existent_network_name, e)
            if message: messages.append(message)
            if error: errors.append(error)            

         
    messages = [str(m) for m in messages if m is not None]
    errors = [str(e) for e in errors if e is not None]

    if len(errors):
        return JsonResponse({'status':False, 'errors':errors, 'messages':messages})
    return JsonResponse({'status':True, 'messages':messages})

