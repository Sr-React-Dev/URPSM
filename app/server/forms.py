from __future__ import absolute_import, unicode_literals
from django import forms
from location_field.widgets import LocationWidget
from .models import Server
from .utils import FrontImageWidget
# from versatileimagefield.forms import SizedImageCenterpointClickDjangoAdminField
from smart_selects.widgets import ChainedSelect
from django import forms


class RegisterServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields= ['name','server_phone','server_email','city','country']


class ServerCreationForm(forms.ModelForm):
    # logo = SizedImageCenterpointClickDjangoAdminField(required=False)
    class Meta:
        model = Server
        exclude = ('rank', 'level')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Server name'}),
            'server_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+212612345678'}),
            'server_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'foo@example.com'}),
            'vat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'credit': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '0', 'type': 'number', 'min': '1'}),

            # 'city': forms.Select(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'city': ChainedSelect(
                app_name='simplecities',
                model_name='city',
                chain_field='country',
                model_field='country',
                show_all=False,
                auto_choose=False,
                attrs={'class': 'form-control'},
                # select2_options={'width': '100%'}
            ),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Server address'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': LocationWidget(attrs={'class': 'form-control'}),
            'logo': FrontImageWidget(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter'}),
            'google_plus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Plus'}),
            'paypal_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your paypal account email'}),
        }



class ServerUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Server
        exclude = ('balance', 'rank', 'level')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Server name'}),
            'server_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+212612345678'}),
            'server_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'foo@example.com'}),
            'vat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            # 'city': forms.Select(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'city': ChainedSelect(
                app_name='simplecities',
                model_name='city',
                chain_field='country',
                model_field='country',
                show_all=False,
                auto_choose=False,
                attrs={'class': 'form-control'},
                # select2_options={'width': '100%'}
            ),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Server address'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': LocationWidget(attrs={'class': 'form-control'}),
            'logo': FrontImageWidget(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter'}),
            'google_plus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Plus'}),
            'paypal_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your paypal account email'}),
        }


class ServerContact(forms.Form):
    server = forms.CharField(widget=forms.HiddenInput())
    component = forms.CharField(widget=forms.HiddenInput())
    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Message'}))
