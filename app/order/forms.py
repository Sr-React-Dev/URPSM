# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.core.exceptions import ValidationError
from django import forms
from .models import ServerOrder
from app.endpoint.models import Endpoint, Network
from smart_selects.widgets import ChainedSelect
from app.antifraud.validators import validate_imei


class ServerOrderForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(ServerOrderForm, self).__init__(*args, **kwargs)

    def clean_imei(self):
        validate_imei(self.cleaned_data.get('imei'))
        return self.cleaned_data.get('imei')

    class Meta:

        model = ServerOrder
        fields = ('endpoint', 'service', 'imei', 'brand', 'model')
        widgets = {
            'imei': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Imei'}),
            'brand': forms.Select(
                attrs={'class': 'form-control searchselect'}
            ),
            'model': ChainedSelect(
                app_name='phone',
                model_name='model',
                chain_field='brand',
                model_field='brand',
                show_all=False,
                auto_choose=False,
                attrs={'class': 'form-control searchselect'},
                # select2_options={"width": "100%"}
            ),
        }
