from __future__ import absolute_import
# from django.core.exceptions import ValidationError
import ast, json
from django import forms
# from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Endpoint, Network
from app.dhrufusion.client import Client as DhruClient
from app.nakshfusion.client import Client as NakshSoftClient
from braces.forms import UserKwargModelFormMixin
from django.utils.html import mark_safe

CHOICES = None
NOT_CHOICES = None

class EndPointNetworkForm(UserKwargModelFormMixin, forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(EndPointNetworkForm, self).__init__(*args, **kwargs)
    
        endpoint = getattr(self, 'instance', None)
        networks = endpoint.client.get_imei_service_list(True)
        existing_networks = endpoint.networks
        existing_services = []
        for n in existing_networks.all():
            services = ast.literal_eval(n.services)
            for key, value in services.iteritems():
                if not key == u'network':
                    existing_services.append((key, value))

      
        CHOICES  = tuple()
        NOT_CHOICES  = tuple()
        for name, services in networks.iteritems():
            choice = (name, )
            not_choice = (name, )
            _services = tuple()
            _existing = tuple()
            for service in services:
                if not service[1] in existing_services:
                    _services = _services + (service[1],)
                else:
                    _existing = _existing + (service[1],) 
                
            if len(_services):
                choice = choice + (_services,)
                CHOICES = CHOICES + (choice,)
            if len(_existing):
                not_choice = not_choice + (_existing,)
                NOT_CHOICES = NOT_CHOICES + (not_choice,)

    

        self.fields['networks'].choices = CHOICES
        self.fields['networks_to'].choices = NOT_CHOICES
        


    networks = forms.ChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id':'id_networks' ,'size':'11' ,'multiple':'multiple' }))
    networks_to = forms.ChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id':'id_networks_to' ,'size':'11' ,'multiple':'multiple' }))
    class Meta:
       model = Endpoint 
       exclude = '__all__'
      

class EndPointForm(forms.ModelForm):
    # captcha = NoReCaptchaField(gtag_attrs={'data-theme': 'light'})

    def clean(self):
        # checking the api access and validate it
        cleaned_data = super(EndPointForm, self).clean()
        url = self.cleaned_data.get('url')
        username = self.cleaned_data.get('username')
        key = self.cleaned_data.get('key')
        provider = self.cleaned_data.get('provider')

        if url and username and key:
            if provider == 'dhru':
                c = DhruClient(dhrufusion_url=url,
                           username=username, apiaccesskey=key)
                if not c.status():
                    self.add_error(
                        'url', 'Please verify your api information either url/username/key are wrong or your api is already used by an other application if so clear the IP in your panel')
            if provider == 'naksh':
                c = NakshSoftClient(nakshfusion_url=url,
                           userId=username, apiKey=key)
                if not c.status():
                    self.add_error(
                        'url', 'Please verify your api information either url/username/key are wrong or your api is already used by an other application if so clear the IP in your panel')
        return cleaned_data

    class Meta:
        model = Endpoint
        fields = ('url', 'username', 'key', 'provider' )
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'API URL'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'API USERNAME'}),
            'key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'API KEY'}),
            'provider': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Provider SERVICE'}),
        }


from app.search.forms import SearchForm

class ServerEndpointNetworkSearchForm(SearchForm):
    def search():
        backend = get_search_backend('default')
        query = self.cleaned_data['q']